"""Private key models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class PrivateKeyModel(CoolipyBaseModel):
    """A private key as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    description: str | None = None
    private_key: str | None = None
    public_key: str | None = None
    fingerprint: str | None = None
    is_git_related: bool | None = None
    team_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PrivateKeyCreateModel(CoolipyBaseModel):
    """Body for creating a private key."""

    name: str | None = None
    description: str | None = None
    private_key: str | None = None


class PrivateKeyUpdateModel(CoolipyBaseModel):
    """Body for updating a private key."""

    name: str | None = None
    description: str | None = None
    private_key: str | None = None
