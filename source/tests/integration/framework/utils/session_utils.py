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

import json
import logging
import time
from typing import Any

from ideadatamodel import (  # type: ignore
    GetSessionConnectionInfoRequest,
    GetSessionInfoRequest,
    ListSessionsRequest,
    VirtualDesktopBaseOS,
    VirtualDesktopSession,
    VirtualDesktopSessionConnectionInfo,
    VirtualDesktopSessionState,
)
from tests.integration.framework.client.res_client import ResClient
from tests.integration.framework.utils.remote_command_runner import (
    EC2InstancePlatform,
    RemoteCommandRunner,
)

logger = logging.getLogger(__name__)

SESSION_COMPLETE_STATES = [
    VirtualDesktopSessionState.READY,
    VirtualDesktopSessionState.ERROR,
    VirtualDesktopSessionState.STOPPED,
    VirtualDesktopSessionState.DELETED,
]
# AWS credentials on CodeBuild expires in an hour.
# Make sure to leave enough time for the test setup and cleanup when running in the code pipeline.
MAX_WAITING_TIME_FOR_LAUNCHING_SESSION_IN_SEC = 2700
MAX_WAITING_TIME_FOR_DELETING_SESSION_IN_SEC = 300
MAX_WAITING_TIME_FOR_STOPPING_IDLE_SESSION_IN_SEC = 1200
MAX_WAITING_TIME_FOR_SESSION_CONNECTION_COUNT_IN_SEC = 300


def wait_for_launching_session(
    client: ResClient, session: VirtualDesktopSession
) -> VirtualDesktopSession:
    start_time = time.time()
    while time.time() - start_time < MAX_WAITING_TIME_FOR_LAUNCHING_SESSION_IN_SEC:
        get_session_info_request = GetSessionInfoRequest(session=session)
        get_session_info_response = client.get_session_info(get_session_info_request)
        session = get_session_info_response.session
        session_state = session.state

        if session_state in SESSION_COMPLETE_STATES:
            assert (
                session_state == VirtualDesktopSessionState.READY
            ), f"Session {session.name} is in an unexpected state {session_state}: {session.failure_reason}"

            return session

        logger.debug(f"session state: {session_state}")
        time.sleep(30)

    assert (
        False
    ), f"Failed to launch session {session.name} within {MAX_WAITING_TIME_FOR_LAUNCHING_SESSION_IN_SEC} seconds"


def wait_for_deleting_session(
    client: ResClient, session: VirtualDesktopSession
) -> None:
    start_time = time.time()
    while time.time() - start_time < MAX_WAITING_TIME_FOR_DELETING_SESSION_IN_SEC:
        list_sessions_response = client.list_sessions(ListSessionsRequest())
        existing_sessions = list_sessions_response.listing

        if existing_sessions and any(
            existing_session.idea_session_id == session.idea_session_id
            for existing_session in existing_sessions
        ):
            logger.debug(f"session {session.idea_session_id} is still available")
            time.sleep(30)
        else:
            return

    assert (
        False
    ), f"Failed to delete session {session.dcv_session_id} within {MAX_WAITING_TIME_FOR_DELETING_SESSION_IN_SEC} seconds"


def wait_for_stopped_idle_session(
    client: ResClient, session: VirtualDesktopSession
) -> None:
    start_time = time.time()
    while time.time() - start_time < MAX_WAITING_TIME_FOR_STOPPING_IDLE_SESSION_IN_SEC:
        get_session_info_request = GetSessionInfoRequest(session=session)
        get_session_info_response = client.get_session_info(get_session_info_request)
        session = get_session_info_response.session
        session_state = session.state

        if session_state == VirtualDesktopSessionState.STOPPED_IDLE:
            return

        logger.debug(f"session state: {session_state}")
        time.sleep(30)

    assert (
        False
    ), f"Failed to stop idle session {session.name} within {MAX_WAITING_TIME_FOR_STOPPING_IDLE_SESSION_IN_SEC} seconds"


"""
Force the auto stop script to run on a session by setting the idle config to an idle timeout threshold of 0
LINUX: Overwrites the existing idle config file
WINDOWS: Writes a new idle config file due to a race condition where the Idle_Config file is typically not created before the integ test runs
"""


def force_idle_session(
    region: str, session: VirtualDesktopSession, env_name: str
) -> None:
    logger.info(f"Setting {session.name} session config to idle...")
    forced_idle_cpu_threshold = 100
    forced_idle_timeout = 0
    platform = (
        EC2InstancePlatform.WINDOWS
        if session.software_stack.base_os == VirtualDesktopBaseOS.WINDOWS
        else EC2InstancePlatform.LINUX
    )
    remote_command_runner = RemoteCommandRunner(region, platform)
    if platform == EC2InstancePlatform.LINUX:
        linux_idle_config_path = "/opt/idea/.idle_config.json"
        commands = [
            "sudo su -",
            f"cat <<< $(jq '.idle_cpu_threshold = {forced_idle_cpu_threshold} | .idle_timeout = {forced_idle_timeout}' {linux_idle_config_path}) > {linux_idle_config_path}",
        ]
    else:
        windows_idle_config_path = "C:\IDEA\Idle_Config.json"
        vdi_helper_api_gateway_url_lookup_key = (
            r"{\"key\": {\"S\": \"vdc.vdi_helper_api_gateway_url\"}}"
        )
        cluster_settings_table_name = f"{env_name}.cluster-settings"
        transition_state = "Stop"
        commands = [
            f"$vdi_helper_api_gateway_url_item = aws dynamodb get-item --table-name {cluster_settings_table_name} --key '{vdi_helper_api_gateway_url_lookup_key}' --region {region} | ConvertFrom-Json",
            "$vdi_helper_api_gateway_url = $vdi_helper_api_gateway_url_item.Item.value.S",
            "$idle_config = New-Object PSObject",
            f"$idle_config | Add-Member -MemberType NoteProperty -Name 'idle_cpu_threshold' -Value '{forced_idle_cpu_threshold}'",
            f"$idle_config | Add-Member -MemberType NoteProperty -Name 'idle_timeout' -Value '{forced_idle_timeout}'",
            f"$idle_config | Add-Member -MemberType NoteProperty -Name 'vdi_helper_api_url' -Value $vdi_helper_api_gateway_url",
            f"$idle_config | Add-Member -MemberType NoteProperty -Name 'transition_state' -Value '{transition_state}'",
            f"$idle_config | ConvertTo-Json | Set-Content -Path '{windows_idle_config_path}' -Encoding UTF8",
        ]

    remote_command_runner.run(session.server.instance_id, commands)


def wait_for_session_connection_count(
    region: str, session: VirtualDesktopSession, count: int
) -> None:
    start_time = time.time()
    while (
        time.time() - start_time < MAX_WAITING_TIME_FOR_SESSION_CONNECTION_COUNT_IN_SEC
    ):
        platform = (
            EC2InstancePlatform.WINDOWS
            if session.software_stack.base_os == VirtualDesktopBaseOS.WINDOWS
            else EC2InstancePlatform.LINUX
        )
        dcv_session_info = describe_dcv_session(
            region, session.server.instance_id, session.dcv_session_id, platform
        )

        num_of_connections = dcv_session_info["num-of-connections"]
        if num_of_connections is not None and num_of_connections == count:
            return

        logger.debug(f"num of connections: {num_of_connections}")
        time.sleep(30)

    assert (
        False
    ), f"Failed to reach session connection count {count} within {MAX_WAITING_TIME_FOR_SESSION_CONNECTION_COUNT_IN_SEC} seconds"


def describe_dcv_session(
    region: str,
    server_instance_id: str,
    dcv_session_id: str,
    platform: EC2InstancePlatform,
) -> Any:
    remote_command_runner = RemoteCommandRunner(region, platform)
    if platform == EC2InstancePlatform.LINUX:
        commands = [f"sudo dcv describe-session {dcv_session_id} -j"]
    else:
        commands = [
            rf'&"C:\Program Files\NICE\DCV\Server\bin\dcv.exe" describe-session {dcv_session_id} -j'
        ]

    output = remote_command_runner.run(server_instance_id, commands)
    try:
        dcv_session_info = json.loads(output)
    except json.JSONDecodeError as e:
        assert False, e

    return dcv_session_info
