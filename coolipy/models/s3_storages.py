"""S3 storage models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class S3StorageModel(CoolipyBaseModel):
    """An S3 storage as returned by the API."""

    uuid: str | None = None
    name: str | None = None
    description: str | None = None
    endpoint: str | None = None
    bucket: str | None = None
    region: str | None = None
    is_usable: bool | None = None
    team_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class S3StorageCreateModel(CoolipyBaseModel):
    """Body for creating an S3 storage."""

    name: str | None = None
    description: str | None = None
    endpoint: str | None = None
    bucket: str | None = None
    region: str | None = None
    key: str | None = None
    secret: str | None = None
    is_usable: bool | None = None


class S3StorageUpdateModel(CoolipyBaseModel):
    """Body for updating an S3 storage."""

    name: str | None = None
    description: str | None = None
    endpoint: str | None = None
    bucket: str | None = None
    region: str | None = None
    key: str | None = None
    secret: str | None = None
    is_usable: bool | None = None
