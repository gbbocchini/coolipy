"""Server models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.enums import ProxyType
from coolipy.models.base import CoolipyBaseModel


class ServerSetting(CoolipyBaseModel):
    """Server settings returned as part of a server model."""

    id: int | None = None
    concurrent_builds: int | None = None
    deployment_queue_limit: int | None = None
    dynamic_timeout: int | None = None
    force_disabled: bool | None = None
    force_server_cleanup: bool | None = None
    is_build_server: bool | None = None
    is_cloudflare_tunnel: bool | None = None
    is_jump_server: bool | None = None
    is_logdrain_axiom_enabled: bool | None = None
    is_logdrain_custom_enabled: bool | None = None
    is_logdrain_highlight_enabled: bool | None = None
    is_logdrain_newrelic_enabled: bool | None = None
    is_metrics_enabled: bool | None = None
    is_reachable: bool | None = None
    is_sentinel_enabled: bool | None = None
    is_swarm_manager: bool | None = None
    is_swarm_worker: bool | None = None
    is_terminal_enabled: bool | None = None
    is_usable: bool | None = None
    logdrain_axiom_api_key: str | None = None
    logdrain_axiom_dataset_name: str | None = None
    logdrain_custom_config: str | None = None
    logdrain_custom_config_parser: str | None = None
    logdrain_highlight_project_id: str | None = None
    logdrain_newrelic_base_uri: str | None = None
    logdrain_newrelic_license_key: str | None = None
    sentinel_metrics_history_days: int | None = None
    sentinel_metrics_refresh_rate_seconds: int | None = None
    sentinel_token: str | None = None
    docker_cleanup_frequency: str | None = None
    docker_cleanup_threshold: int | None = None
    server_id: int | None = None
    wildcard_domain: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    delete_unused_volumes: bool | None = None
    delete_unused_networks: bool | None = None
    connection_timeout: int | None = None


class ServerModel(CoolipyBaseModel):
    """A server as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    description: str | None = None
    ip: str | None = None
    user: str | None = None
    port: int | None = None
    proxy: dict | None = None
    proxy_type: str | None = None
    is_coolify_host: bool | None = None
    is_reachable: bool | None = None
    is_usable: bool | None = None
    high_disk_usage_notification_sent: bool | None = None
    unreachable_notification_sent: bool | None = None
    unreachable_count: int | None = None
    validation_logs: str | None = None
    log_drain_notification_sent: bool | None = None
    swarm_cluster: str | None = None
    settings: ServerSetting | None = None


class ServerCreateModel(CoolipyBaseModel):
    """Body for creating a server."""

    name: str | None = None
    description: str | None = None
    ip: str | None = None
    port: int | None = None
    user: str | None = None
    private_key_uuid: str | None = None
    is_build_server: bool | None = None
    instant_validate: bool | None = None
    proxy_type: ProxyType | None = None


class ServerUpdateModel(CoolipyBaseModel):
    """Body for updating a server."""

    name: str | None = None
    description: str | None = None
    ip: str | None = None
    port: int | None = None
    user: str | None = None
    private_key_uuid: str | None = None
    is_build_server: bool | None = None
    instant_validate: bool | None = None
    proxy_type: ProxyType | None = None
    concurrent_builds: int | None = None
    dynamic_timeout: int | None = None
    deployment_queue_limit: int | None = None
    server_disk_usage_notification_threshold: int | None = None
    server_disk_usage_check_frequency: str | None = None
    connection_timeout: int | None = None
