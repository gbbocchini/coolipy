"""Service models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class ServiceURL(CoolipyBaseModel):
    """A per-service URL mapping for docker-compose services."""

    name: str | None = None
    url: str | None = None


class ServiceModel(CoolipyBaseModel):
    """A service as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    environment_id: int | None = None
    server_id: int | None = None
    description: str | None = None
    docker_compose_raw: str | None = None
    docker_compose: str | None = None
    destination_type: str | None = None
    destination_id: int | None = None
    connect_to_docker_network: bool | None = None
    is_container_label_escape_enabled: bool | None = None
    is_container_label_readonly_enabled: bool | None = None
    config_hash: str | None = None
    service_type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ServiceCreateModel(CoolipyBaseModel):
    """Body for creating a service (one-click or custom)."""

    type: str | None = None
    name: str | None = None
    description: str | None = None
    project_uuid: str | None = None
    environment_name: str | None = None
    environment_uuid: str | None = None
    server_uuid: str | None = None
    destination_uuid: str | None = None
    instant_deploy: bool | None = None
    docker_compose_raw: str | None = None
    urls: list[ServiceURL] | None = None
    force_domain_override: bool | None = None
    is_container_label_escape_enabled: bool | None = None
    tags: list[str] | None = None


class ServiceUpdateModel(CoolipyBaseModel):
    """Body for updating a service."""

    name: str | None = None
    description: str | None = None
    docker_compose_raw: str | None = None
    is_container_label_escape_enabled: bool | None = None
    force_domain_override: bool | None = None
    urls: list[ServiceURL] | None = None
