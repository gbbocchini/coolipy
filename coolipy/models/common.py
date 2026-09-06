"""Shared models reused across multiple coolipy resources."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from coolipy.models.base import CoolipyBaseModel


class EnvironmentVariable(CoolipyBaseModel):
    """An environment variable as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    resourceable_type: str | None = None
    resourceable_id: int | None = None
    is_literal: bool | None = None
    is_multiline: bool | None = None
    is_preview: bool | None = None
    is_runtime: bool | None = None
    is_buildtime: bool | None = None
    is_shared: bool | None = None
    is_shown_once: bool | None = None
    key: str | None = None
    value: str | None = None
    real_value: str | None = None
    comment: str | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EnvironmentVariableCreate(CoolipyBaseModel):
    """Body for creating an environment variable."""

    key: str | None = None
    value: str | None = None
    is_preview: bool | None = None
    is_literal: bool | None = None
    is_multiline: bool | None = None
    is_shown_once: bool | None = None


class EnvironmentVariableUpdate(CoolipyBaseModel):
    """Body for updating an environment variable."""

    key: str | None = None
    value: str | None = None
    is_preview: bool | None = None
    is_literal: bool | None = None
    is_multiline: bool | None = None
    is_shown_once: bool | None = None


class BulkEnvsUpdate(CoolipyBaseModel):
    """Body for bulk-updating environment variables."""

    data: list[EnvironmentVariableCreate] = Field(default_factory=list)


class ScheduledTask(CoolipyBaseModel):
    """A scheduled task as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    enabled: bool | None = None
    name: str | None = None
    command: str | None = None
    frequency: str | None = None
    container: str | None = None
    timeout: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ScheduledTaskCreate(CoolipyBaseModel):
    """Body for creating a scheduled task."""

    enabled: bool | None = None
    name: str | None = None
    command: str | None = None
    frequency: str | None = None
    container: str | None = None
    timeout: int | None = None


class ScheduledTaskUpdate(CoolipyBaseModel):
    """Body for updating a scheduled task."""

    enabled: bool | None = None
    name: str | None = None
    command: str | None = None
    frequency: str | None = None
    container: str | None = None
    timeout: int | None = None


class ScheduledTaskExecution(CoolipyBaseModel):
    """An execution of a scheduled task."""

    uuid: str | None = None
    status: str | None = None
    message: str | None = None
    retry_count: int | None = None
    duration: float | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Destination(CoolipyBaseModel):
    """A Docker network destination attached to a server."""

    uuid: str | None = None
    name: str | None = None
    network: str | None = None
    type: str | None = None
    server_uuid: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DestinationCreate(CoolipyBaseModel):
    """Body for creating a destination."""

    name: str | None = None
    network: str | None = None
    type: str | None = None


class Tag(CoolipyBaseModel):
    """A tag attached to a resource."""

    uuid: str | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TagCreate(CoolipyBaseModel):
    """Body for creating a global tag."""

    name: str | None = None


class TagUpdate(CoolipyBaseModel):
    """Body for updating a global tag."""

    name: str | None = None


class Logs(CoolipyBaseModel):
    """Log output returned by a logs endpoint."""

    logs: str | None = None


class MessageResponse(CoolipyBaseModel):
    """A response carrying a single ``message``."""

    message: str | None = None


class UUIDResponse(CoolipyBaseModel):
    """A response carrying a single ``uuid``."""

    uuid: str | None = None


class DeploymentQueuedResponse(CoolipyBaseModel):
    """A response indicating a deployment was queued."""

    message: str | None = None
    deployment_uuid: str | None = None


class StorageCreate(CoolipyBaseModel):
    """Body for creating a persistent or file storage."""

    type: str | None = None
    name: str | None = None
    mount_path: str | None = None
    host_path: str | None = None
    content: str | None = None
    is_directory: bool | None = None
    fs_path: str | None = None


class StorageUpdate(CoolipyBaseModel):
    """Body for updating a persistent or file storage."""

    uuid: str | None = None
    id: int | None = None
    type: str | None = None
    is_preview_suffix_enabled: bool | None = None
    name: str | None = None
    mount_path: str | None = None
    host_path: str | None = None
    content: str | None = None


class TagsCreate(CoolipyBaseModel):
    """Body for adding one or more tags to a resource."""

    tag_name: str | None = None
    tag_names: list[str] | None = None


class VolumeBackupScheduleRequest(CoolipyBaseModel):
    """Body for scheduling volume backups."""

    frequency: str | None = None
    enabled: bool | None = None
    save_s3: bool | None = None
    disable_local_backup: bool | None = None
    stop_during_backup: bool | None = None
    s3_storage_uuid: str | None = None
    retention_amount_locally: int | None = None
    retention_days_locally: int | None = None
    retention_max_storage_locally: float | None = None
    retention_amount_s3: int | None = None
    retention_days_s3: int | None = None
    retention_max_storage_s3: float | None = None
    timeout: int | None = None


class VolumeBackupScheduleResponse(CoolipyBaseModel):
    """A scheduled volume backup as returned by the API."""

    uuid: str | None = None
    message: str | None = None
    storage_uuid: str | None = None
    storage_type: str | None = None
    frequency: str | None = None
    enabled: bool | None = None
    save_s3: bool | None = None
    disable_local_backup: bool | None = None
    stop_during_backup: bool | None = None
    s3_storage_uuid: str | None = None
    retention_amount_locally: int | None = None
    retention_days_locally: int | None = None
    retention_max_storage_locally: float | None = None
    retention_amount_s3: int | None = None
    retention_days_s3: int | None = None
    retention_max_storage_s3: float | None = None
    timeout: int | None = None
