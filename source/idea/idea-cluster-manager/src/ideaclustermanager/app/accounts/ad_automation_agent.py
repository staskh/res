#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
#  with the License. A copy of the License is located at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
#  and limitations under the License.


from ideasdk.service import SocaService
from ideasdk.context import SocaContext
from ideasdk.utils import Utils
from ideadatamodel import exceptions, errorcodes

from ideaclustermanager.app.accounts.db.ad_automation_dao import ADAutomationDAO
from ideaclustermanager.app.accounts.helpers.preset_computer_helper import PresetComputeHelper

from typing import Dict
from threading import Thread, Event
import ldap  # noqa

DEFAULT_MAX_MESSAGES = 1
DEFAULT_WAIT_INTERVAL_SECONDS = 20

AD_RESET_PASSWORD_LOCK_KEY = 'activedirectory.reset-password'


class ADAutomationAgent(SocaService):
    """
    IDEA - Active Directory Automation Agent

    * Manages password rotation of AD Admin credentials
    * Manages automation for creating preset-computers using adcli for cluster nodes

    Developer Note:
    * Expect admins to heavily customize this implementation
    """

    def __init__(self, context: SocaContext):
        super().__init__(context)
        self.context = context
        self.logger = context.logger('ad-automation-agent')

        self.ad_automation_sqs_queue_url = self.context.config().get_string('directoryservice.ad_automation.sqs_queue_url', required=True)

        self.ad_automation_dao = ADAutomationDAO(context=self.context)
        self.ad_automation_dao.initialize()

        self._stop_event = Event()
        self._automation_thread = Thread(name='ad-automation-thread', target=self.automation_loop)

    def automation_loop(self):

        while not self._stop_event.is_set():

            admin_user_ok = False

            try:
                admin_user_ok = True

                visibility_timeout = self.context.config().get_int('directoryservice.ad_automation.sqs_visibility_timeout_seconds', default=30)
                result = self.context.aws().sqs().receive_message(
                    QueueUrl=self.ad_automation_sqs_queue_url,
                    MaxNumberOfMessages=DEFAULT_MAX_MESSAGES,
                    WaitTimeSeconds=DEFAULT_WAIT_INTERVAL_SECONDS,
                    AttributeNames=['SenderId'],
                    VisibilityTimeout=visibility_timeout
                )

                sqs_messages = Utils.get_value_as_list('Messages', result, [])

                delete_messages = []

                def add_to_delete(sqs_message_: Dict):
                    delete_messages.append({
                        'Id': sqs_message_['MessageId'],
                        'ReceiptHandle': sqs_message_['ReceiptHandle']
                    })

                for sqs_message in sqs_messages:
                    try:

                        message_body = Utils.get_value_as_string('Body', sqs_message)

                        request = Utils.from_json(message_body)
                        header = Utils.get_value_as_dict('header', request)
                        namespace = Utils.get_value_as_string('namespace', header)

                        # todo - constants for the namespaces supported
                        ad_automation_namespaces = {'ADAutomation.PresetComputer', 'ADAutomation.UpdateComputerDescription', 'ADAutomation.DeleteComputer'}
                        if namespace not in ad_automation_namespaces:
                            self.logger.error(f'Invalid request: namespace {namespace} not supported. Supported namespaces: {ad_automation_namespaces}')
                            add_to_delete(sqs_message)
                            continue

                        attributes = Utils.get_value_as_dict('Attributes', sqs_message, {})
                        sender_id = Utils.get_value_as_string('SenderId', attributes)

                        self.logger.info(f'Processing AD automation event: {namespace}')

                        try:

                            if namespace == 'ADAutomation.PresetComputer':
                                PresetComputeHelper(
                                    context=self.context,
                                    ad_automation_dao=self.ad_automation_dao,
                                    sender_id=sender_id,
                                    request=request
                                ).invoke()
                            elif namespace == 'ADAutomation.DeleteComputer':
                                self.logger.debug('Processing AD automation event: DeleteComputer')
                            elif namespace == 'ADAutomation.UpdateComputerDescription':
                                self.logger.debug('Processing AD automation event: UpdateComputerDescription')

                            # no exception, AD automation succeeded. delete from queue.
                            add_to_delete(sqs_message)

                        except exceptions.SocaException as e:
                            if e.error_code == errorcodes.AD_AUTOMATION_PRESET_COMPUTER_FAILED:
                                self.logger.error(f'{e}')
                                add_to_delete(sqs_message)
                            elif e.error_code == errorcodes.AD_AUTOMATION_PRESET_COMPUTER_RETRY:
                                # do nothing. request will be retried after visibility timeout interval.
                                self.logger.warning(f'{e} - request will be retried in {visibility_timeout} seconds')
                            else:
                                # retry on any unhandled exception.
                                raise e

                    except Exception as e:
                        self.logger.exception(f'failed to process sqs message: {e}. payload: {Utils.to_json(sqs_message)}. processing will be retried in {visibility_timeout} seconds ...')

                if len(delete_messages) > 0:
                    delete_message_result = self.context.aws().sqs().delete_message_batch(
                        QueueUrl=self.ad_automation_sqs_queue_url,
                        Entries=delete_messages
                    )
                    failed = Utils.get_value_as_list('Failed', delete_message_result, [])
                    if len(failed) > 0:
                        self.logger.error(f'Failed to delete AD automation entries. This could result in an infinite loop. Consider increasing the directoryservice.ad_automation.sqs_visibility_timeout_seconds. failed messages: {failed}')

            except KeyboardInterrupt:
                pass
            except Exception as e:
                self.logger.exception(f'ad automation failure: {e}')
            finally:
                # wait only if admin user is not OK and keep retrying.
                # if admin user and/or credentials are ok, wait will be handled by sqs receive message long polling
                if not admin_user_ok:
                    self._stop_event.wait(DEFAULT_WAIT_INTERVAL_SECONDS)

    def start(self):
        self.logger.info('starting ad automation agent ...')
        self._automation_thread.start()

    def stop(self):
        self.logger.info('stopping ad automation agent ...')
        self._stop_event.set()
        self._automation_thread.join()
