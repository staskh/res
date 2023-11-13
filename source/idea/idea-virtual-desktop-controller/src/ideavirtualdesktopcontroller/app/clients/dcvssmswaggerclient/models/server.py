# coding: utf-8

"""
    DCV Session Manager

    DCV Session Manager API  # noqa: E501

    OpenAPI spec version: 2021.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class Server(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'ip': 'str',
        'hostname': 'str',
        'default_dns_name': 'str',
        'port': 'str',
        'endpoints': 'list[Endpoint]',
        'web_url_path': 'str',
        'version': 'str',
        'session_manager_agent_version': 'str',
        'availability': 'str',
        'unavailability_reason': 'str',
        'console_session_count': 'int',
        'virtual_session_count': 'int',
        'host': 'Host',
        'tags': 'list[KeyValuePair]'
    }

    attribute_map = {
        'id': 'Id',
        'ip': 'Ip',
        'hostname': 'Hostname',
        'default_dns_name': 'DefaultDnsName',
        'port': 'Port',
        'endpoints': 'Endpoints',
        'web_url_path': 'WebUrlPath',
        'version': 'Version',
        'session_manager_agent_version': 'SessionManagerAgentVersion',
        'availability': 'Availability',
        'unavailability_reason': 'UnavailabilityReason',
        'console_session_count': 'ConsoleSessionCount',
        'virtual_session_count': 'VirtualSessionCount',
        'host': 'Host',
        'tags': 'Tags'
    }

    def __init__(self, id=None, ip=None, hostname=None, default_dns_name=None, port=None, endpoints=None, web_url_path=None, version=None, session_manager_agent_version=None, availability=None, unavailability_reason=None, console_session_count=None, virtual_session_count=None, host=None, tags=None):  # noqa: E501
        """Server - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._ip = None
        self._hostname = None
        self._default_dns_name = None
        self._port = None
        self._endpoints = None
        self._web_url_path = None
        self._version = None
        self._session_manager_agent_version = None
        self._availability = None
        self._unavailability_reason = None
        self._console_session_count = None
        self._virtual_session_count = None
        self._host = None
        self._tags = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if ip is not None:
            self.ip = ip
        if hostname is not None:
            self.hostname = hostname
        if default_dns_name is not None:
            self.default_dns_name = default_dns_name
        if port is not None:
            self.port = port
        if endpoints is not None:
            self.endpoints = endpoints
        if web_url_path is not None:
            self.web_url_path = web_url_path
        if version is not None:
            self.version = version
        if session_manager_agent_version is not None:
            self.session_manager_agent_version = session_manager_agent_version
        if availability is not None:
            self.availability = availability
        if unavailability_reason is not None:
            self.unavailability_reason = unavailability_reason
        if console_session_count is not None:
            self.console_session_count = console_session_count
        if virtual_session_count is not None:
            self.virtual_session_count = virtual_session_count
        if host is not None:
            self.host = host
        if tags is not None:
            self.tags = tags

    @property
    def id(self):
        """Gets the id of this Server.  # noqa: E501

        The id of the server  # noqa: E501

        :return: The id of this Server.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Server.

        The id of the server  # noqa: E501

        :param id: The id of this Server.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def ip(self):
        """Gets the ip of this Server.  # noqa: E501

        The ip of the server  # noqa: E501

        :return: The ip of this Server.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this Server.

        The ip of the server  # noqa: E501

        :param ip: The ip of this Server.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def hostname(self):
        """Gets the hostname of this Server.  # noqa: E501

        The hostname of the server  # noqa: E501

        :return: The hostname of this Server.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this Server.

        The hostname of the server  # noqa: E501

        :param hostname: The hostname of this Server.  # noqa: E501
        :type: str
        """

        self._hostname = hostname

    @property
    def default_dns_name(self):
        """Gets the default_dns_name of this Server.  # noqa: E501

        The default DNS name of the server  # noqa: E501

        :return: The default_dns_name of this Server.  # noqa: E501
        :rtype: str
        """
        return self._default_dns_name

    @default_dns_name.setter
    def default_dns_name(self, default_dns_name):
        """Sets the default_dns_name of this Server.

        The default DNS name of the server  # noqa: E501

        :param default_dns_name: The default_dns_name of this Server.  # noqa: E501
        :type: str
        """

        self._default_dns_name = default_dns_name

    @property
    def port(self):
        """Gets the port of this Server.  # noqa: E501

        The port where the server listens. This field is deprecated and replaced by PortTcp  # noqa: E501

        :return: The port of this Server.  # noqa: E501
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this Server.

        The port where the server listens. This field is deprecated and replaced by PortTcp  # noqa: E501

        :param port: The port of this Server.  # noqa: E501
        :type: str
        """

        self._port = port

    @property
    def endpoints(self):
        """Gets the endpoints of this Server.  # noqa: E501

        The array representing DCV endpoints  # noqa: E501

        :return: The endpoints of this Server.  # noqa: E501
        :rtype: list[Endpoint]
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """Sets the endpoints of this Server.

        The array representing DCV endpoints  # noqa: E501

        :param endpoints: The endpoints of this Server.  # noqa: E501
        :type: list[Endpoint]
        """

        self._endpoints = endpoints

    @property
    def web_url_path(self):
        """Gets the web_url_path of this Server.  # noqa: E501

        The server web url path  # noqa: E501

        :return: The web_url_path of this Server.  # noqa: E501
        :rtype: str
        """
        return self._web_url_path

    @web_url_path.setter
    def web_url_path(self, web_url_path):
        """Sets the web_url_path of this Server.

        The server web url path  # noqa: E501

        :param web_url_path: The web_url_path of this Server.  # noqa: E501
        :type: str
        """

        self._web_url_path = web_url_path

    @property
    def version(self):
        """Gets the version of this Server.  # noqa: E501

        The version of the server  # noqa: E501

        :return: The version of this Server.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Server.

        The version of the server  # noqa: E501

        :param version: The version of this Server.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def session_manager_agent_version(self):
        """Gets the session_manager_agent_version of this Server.  # noqa: E501

        The version of the session manager agent  # noqa: E501

        :return: The session_manager_agent_version of this Server.  # noqa: E501
        :rtype: str
        """
        return self._session_manager_agent_version

    @session_manager_agent_version.setter
    def session_manager_agent_version(self, session_manager_agent_version):
        """Sets the session_manager_agent_version of this Server.

        The version of the session manager agent  # noqa: E501

        :param session_manager_agent_version: The session_manager_agent_version of this Server.  # noqa: E501
        :type: str
        """

        self._session_manager_agent_version = session_manager_agent_version

    @property
    def availability(self):
        """Gets the availability of this Server.  # noqa: E501

        The server availability  # noqa: E501

        :return: The availability of this Server.  # noqa: E501
        :rtype: str
        """
        return self._availability

    @availability.setter
    def availability(self, availability):
        """Sets the availability of this Server.

        The server availability  # noqa: E501

        :param availability: The availability of this Server.  # noqa: E501
        :type: str
        """
        allowed_values = ["AVAILABLE", "UNAVAILABLE"]  # noqa: E501
        if availability not in allowed_values:
            raise ValueError(
                "Invalid value for `availability` ({0}), must be one of {1}"  # noqa: E501
                .format(availability, allowed_values)
            )

        self._availability = availability

    @property
    def unavailability_reason(self):
        """Gets the unavailability_reason of this Server.  # noqa: E501

        The unavailability reason  # noqa: E501

        :return: The unavailability_reason of this Server.  # noqa: E501
        :rtype: str
        """
        return self._unavailability_reason

    @unavailability_reason.setter
    def unavailability_reason(self, unavailability_reason):
        """Sets the unavailability_reason of this Server.

        The unavailability reason  # noqa: E501

        :param unavailability_reason: The unavailability_reason of this Server.  # noqa: E501
        :type: str
        """
        allowed_values = ["SERVER_FULL", "SERVER_CLOSED", "UNREACHABLE_AGENT", "UNHEALTHY_DCV_SERVER", "EXISTING_LOGGED_IN_USER", "UNKNOWN"]  # noqa: E501
        if unavailability_reason not in allowed_values:
            raise ValueError(
                "Invalid value for `unavailability_reason` ({0}), must be one of {1}"  # noqa: E501
                .format(unavailability_reason, allowed_values)
            )

        self._unavailability_reason = unavailability_reason

    @property
    def console_session_count(self):
        """Gets the console_session_count of this Server.  # noqa: E501

        The count of console session on the server  # noqa: E501

        :return: The console_session_count of this Server.  # noqa: E501
        :rtype: int
        """
        return self._console_session_count

    @console_session_count.setter
    def console_session_count(self, console_session_count):
        """Sets the console_session_count of this Server.

        The count of console session on the server  # noqa: E501

        :param console_session_count: The console_session_count of this Server.  # noqa: E501
        :type: int
        """

        self._console_session_count = console_session_count

    @property
    def virtual_session_count(self):
        """Gets the virtual_session_count of this Server.  # noqa: E501

        The count of virtual session on the server  # noqa: E501

        :return: The virtual_session_count of this Server.  # noqa: E501
        :rtype: int
        """
        return self._virtual_session_count

    @virtual_session_count.setter
    def virtual_session_count(self, virtual_session_count):
        """Sets the virtual_session_count of this Server.

        The count of virtual session on the server  # noqa: E501

        :param virtual_session_count: The virtual_session_count of this Server.  # noqa: E501
        :type: int
        """

        self._virtual_session_count = virtual_session_count

    @property
    def host(self):
        """Gets the host of this Server.  # noqa: E501


        :return: The host of this Server.  # noqa: E501
        :rtype: Host
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this Server.


        :param host: The host of this Server.  # noqa: E501
        :type: Host
        """

        self._host = host

    @property
    def tags(self):
        """Gets the tags of this Server.  # noqa: E501

        The tags of the server  # noqa: E501

        :return: The tags of this Server.  # noqa: E501
        :rtype: list[KeyValuePair]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Server.

        The tags of the server  # noqa: E501

        :param tags: The tags of this Server.  # noqa: E501
        :type: list[KeyValuePair]
        """

        self._tags = tags

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Server, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Server):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
