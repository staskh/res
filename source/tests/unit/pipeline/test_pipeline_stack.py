#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
import os
from typing import Any

import aws_cdk
import aws_cdk as cdk
import pytest
from aws_cdk import assertions

from idea.infrastructure.install.parameters.parameters import RESParameters
from idea.infrastructure.install.stacks.install_stack import (
    PUBLIC_REGISTRY_NAME,
    InstallStack,
)
from idea.pipeline.stack import DeployStage, PipelineStack

TEST_CONTEXT = {"repository_name": "mock_repo", "branch_name": "mock_branch"}


@pytest.fixture
def template() -> assertions.Template:
    app = cdk.App(context=TEST_CONTEXT)
    stack = PipelineStack(app, "idea-pipeline")
    template = assertions.Template.from_stack(stack)
    return template


@pytest.fixture(autouse=True)
def patch_get_ecr_repo_arn_from_registry_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_get_ecr_repo_arn_from_registry_name(_: Any, registry_name: str) -> str:

        return "mock-ecr-arn"

    monkeypatch.setattr(
        InstallStack,
        "get_ecr_repo_arn_from_registry_name",
        mock_get_ecr_repo_arn_from_registry_name,
    )


def test_pipeline_created(template: assertions.Template) -> None:
    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)


def test_registry_name_set_correctly_from_context() -> None:
    # No context should be public registry name
    app = aws_cdk.App()
    app.node.set_context("ad_sync_registry_name", "ad_sync")
    stage = DeployStage(
        aws_cdk.App(context={"vpc_id": "vpc-0fakeexample0000001"}),
        "Stage",
        False,
        RESParameters(),
    )

    assert stage.install_stack.installer_registry_name == PUBLIC_REGISTRY_NAME

    # context should override
    app = aws_cdk.App(context={"vpc_id": "vpc-0fakeexample0000001"})
    app.node.set_context("ad_sync_registry_name", "ad_sync")
    app.node.set_context("installer_registry_name", "foo")
    stage = DeployStage(app, "DeployStage", False, RESParameters())

    assert stage.install_stack.installer_registry_name == "foo"
