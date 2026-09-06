"""Deployment models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class DeploymentModel(CoolipyBaseModel):
    """A deployment as returned by the API."""

    id: int | None = None
    application_id: str | None = None
    deployment_uuid: str | None = None
    pull_request_id: int | None = None
    docker_registry_image_tag: str | None = None
    configuration_hash: str | None = None
    configuration_snapshot: dict | None = None
    configuration_diff: dict | None = None
    force_rebuild: bool | None = None
    commit: str | None = None
    status: str | None = None
    is_webhook: bool | None = None
    is_api: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    logs: str | None = None
    current_process_id: str | None = None
    restart_only: bool | None = None
    git_type: str | None = None
    server_id: int | None = None
    application_name: str | None = None
    server_name: str | None = None
    deployment_url: str | None = None
    destination_id: str | None = None
    only_this_server: bool | None = None
    rollback: bool | None = None
    commit_message: str | None = None


class DeploymentEntry(CoolipyBaseModel):
    """A single deployment result returned by the ``deploy`` endpoint."""

    message: str | None = None
    resource_uuid: str | None = None
    deployment_uuid: str | None = None


class DeployResponse(CoolipyBaseModel):
    """Response from the ``deploy`` endpoint."""

    deployments: list[DeploymentEntry] | None = None
