"""Project and environment models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class ProjectModel(CoolipyBaseModel):
    """A project as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    description: str | None = None


class ProjectCreateModel(CoolipyBaseModel):
    """Body for creating a project."""

    name: str | None = None
    description: str | None = None


class ProjectUpdateModel(CoolipyBaseModel):
    """Body for updating a project."""

    name: str | None = None
    description: str | None = None


class EnvironmentModel(CoolipyBaseModel):
    """An environment as returned by the API."""

    id: int | None = None
    name: str | None = None
    project_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    description: str | None = None


class EnvironmentCreateModel(CoolipyBaseModel):
    """Body for creating an environment."""

    name: str | None = None


class EnvironmentUpdateModel(CoolipyBaseModel):
    """Body for updating an environment."""

    name: str | None = None
