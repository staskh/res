#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
import dataclasses
import re

import aws_cdk
import pytest
from aws_cdk.assertions import Template

from idea.infrastructure.install.constants import PROXY_URL_REGEX
from idea.infrastructure.install.parameters.base import Attributes, Base
from idea.infrastructure.install.parameters.common import CommonKey
from idea.infrastructure.install.parameters.directoryservice import DirectoryServiceKey
from idea.infrastructure.install.parameters.parameters import RESParameters
from idea.infrastructure.install.stacks.install_stack import InstallStack


def test_parameters_are_generated(cluster_name: str) -> None:
    parameters = RESParameters(cluster_name=cluster_name)
    env = aws_cdk.Environment(account="111111111111", region="us-east-1")
    app = aws_cdk.App(context={"vpc_id": "vpc-0fakeexample0000001"})
    InstallStack(
        app,
        "IDEAInstallStack",
        parameters=parameters,
        ad_sync_registry_name="ad_sync",
        env=env,
    )

    assert parameters._generated
    assert parameters.cluster_name == cluster_name
    assert parameters.get(CommonKey.CLUSTER_NAME).default == cluster_name
    assert parameters.get(CommonKey.INFRASTRUCTURE_HOST_SUBNETS).default is None


def test_parameters_can_be_passed_via_context() -> None:
    parameters = RESParameters(
        cluster_name="foo", infrastructure_host_subnets=["a", "b"]
    )

    stack = aws_cdk.Stack()
    for key, value in parameters.to_context().items():
        stack.node.set_context(key, value)

    context_params = RESParameters.from_context(stack)

    assert context_params.cluster_name == parameters.cluster_name
    assert (
        context_params.infrastructure_host_subnets
        == parameters.infrastructure_host_subnets
    )


def test_parameter_list_default_set_correctly() -> None:
    parameters = RESParameters(infrastructure_host_subnets=["a", "b"])
    parameters.generate(aws_cdk.Stack())
    assert parameters.get(CommonKey.INFRASTRUCTURE_HOST_SUBNETS).default == "a,b"


def test_fields_only_includes_base_parameters() -> None:
    @dataclasses.dataclass
    class TestParameters(Base):
        name: str = Base.parameter(Attributes(id=CommonKey.CLUSTER_NAME))
        other: str = "not defined as a base parameter"

    fields = list(TestParameters._fields())
    assert len(fields) == 1
    field, attributes = fields[0]
    assert field.name == "name"
    assert attributes.id == CommonKey.CLUSTER_NAME


def test_parameters_only_generates_cfn_parameters_for_base_parameter_attributes(
    stack: InstallStack,
    template: Template,
) -> None:
    parameters = template.find_parameters(logical_id="*")

    cfn_keys = set(parameters.keys())
    defined_keys = set(attributes.id.value for _, attributes in RESParameters._fields())

    assert cfn_keys == defined_keys


@pytest.mark.parametrize(
    "url, expected_valid",
    [
        ("http://192.168.0.1:8080", True),
        ("https://10.0.0.1:3000", True),
        ("", True),  # Empty string is accepted as the parameter is optionl
        ("http://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:80", True),
        (
            "https://[2001:db8::1]:8443",
            False,
        ),  # IPV6 with abbreviation is NOT accepted
        ("http://example.com:8080", False),  # Domain name is NOT accepted
        ("ftp://192.168.0.1:21", False),  # ftp protocol is NOT accepted
        ("http://192.168.0.1", False),  # Port number missing
        ("https://[2001:db8::1]", False),  # Port number missing
    ],
)
def test_proxy_url_regex(url: str, expected_valid: bool) -> None:
    is_valid = bool(re.match(PROXY_URL_REGEX, url))
    assert is_valid == expected_valid
