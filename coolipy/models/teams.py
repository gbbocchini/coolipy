"""Team and user models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class UserModel(CoolipyBaseModel):
    """A user as returned by the API."""

    id: int | None = None
    name: str | None = None
    email: str | None = None
    email_verified_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    two_factor_confirmed_at: datetime | None = None
    force_password_reset: bool | None = None


class TeamModel(CoolipyBaseModel):
    """A team as returned by the API."""

    id: int | None = None
    name: str | None = None
    description: str | None = None
    personal_team: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    show_boarding: bool | None = None
    custom_server_limit: str | None = None
    members: list[UserModel] | None = None
