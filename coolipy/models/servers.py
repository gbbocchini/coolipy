from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, override

from coolipy.constants import _COOLIFY_DEFAULT_PROXY
from coolipy.models.base import CoolipyBaseModel


@dataclass
class ServerProxyModel:
    """
    Coolify Server Proxy data model.
    """

    type: Optional[str] = _COOLIFY_DEFAULT_PROXY
    status: Optional[str] = None
    last_saved_settings: Optional[str] = None
    last_applied_settings: Optional[str] = None
    force_stop: Optional[bool] = None
    redirect_enabled: Optional[bool] = None


@dataclass
class ServerSettingsModel(CoolipyBaseModel):
    """
    Coolify Server Settings data model.
    """

    id: Optional[int] = None
    concurrent_builds: Optional[int] = None
    delete_unused_networks: Optional[bool] = None
    delete_unused_volumes: Optional[bool] = None
    docker_cleanup_frequency: Optional[str] = None
    docker_cleanup_threshold: Optional[int] = None
    dynamic_timeout: Optional[int] = None
    force_disabled: Optional[bool] = None
    force_docker_cleanup: Optional[bool] = None
    generate_exact_labels: Optional[bool] = None
    is_build_server: Optional[bool] = None
    is_cloudflare_tunnel: Optional[bool] = None
    is_jump_server: Optional[bool] = None
    is_logdrain_axiom_enabled: Optional[bool] = None
    is_logdrain_custom_enabled: Optional[bool] = None
    is_logdrain_highlight_enabled: Optional[bool] = None
    is_logdrain_newrelic_enabled: Optional[bool] = None
    is_metrics_enabled: Optional[bool] = None
    is_reachable: Optional[bool] = None
    is_sentinel_debug_enabled: Optional[bool] = None
    is_sentinel_enabled: Optional[bool] = None
    is_swarm_manager: Optional[bool] = None
    is_swarm_worker: Optional[bool] = None
    is_usable: Optional[bool] = None
    sentinel_custom_url: Optional[str] = None
    sentinel_metrics_history_days: Optional[int] = None
    sentinel_metrics_refresh_rate_seconds: Optional[int] = None
    sentinel_push_interval_seconds: Optional[int] = None
    sentinel_token: Optional[str] = None
    server_disk_usage_notification_threshold: Optional[int] = None
    server_id: Optional[int] = None
    server_timezone: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None
    logdrain_axiom_api_key: Optional[str] = None
    logdrain_axiom_dataset_name: Optional[str] = None
    logdrain_custom_config: Optional[str] = None
    logdrain_custom_config_parser: Optional[str] = None
    logdrain_highlight_project_id: Optional[str] = None
    logdrain_newrelic_base_uri: Optional[str] = None
    logdrain_newrelic_license_key: Optional[str] = None
    wildcard_domain: Optional[str] = None
    server_disk_usage_check_frequency: Optional[str] = None


@dataclass
class ServerModel(CoolipyBaseModel):
    """
    Coolify Server data model.
    """

    id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    ip: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    private_key_id: Optional[int] = None
    uuid: Optional[str] = None
    team_id: Optional[int] = None
    sentinel_updated_at: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None
    deleted_at: Optional[Union[str, datetime]] = None
    high_disk_usage_notification_sent: Optional[bool] = False
    log_drain_notification_sent: Optional[bool] = False
    swarm_cluster: Optional[bool] = False
    validation_logs: Optional[str] = None
    unreachable_count: Optional[int] = None
    unreachable_notification_sent: Optional[bool] = False
    proxy: Optional[ServerProxyModel] = None
    settings: Optional[ServerSettingsModel] = None
    is_reachable: Optional[bool] = None
    is_usable: Optional[bool] = None
    is_coolify_host: Optional[bool] = None

    @override
    def _adjust_nested(self):
        if isinstance(self.settings, dict) and self.settings:
            raw_sets = self.settings
            parsed = ServerSettingsModel(**raw_sets).pythonify()
            self.settings = parsed

        raw_proxy = self.proxy

        if raw_proxy and isinstance(raw_proxy, dict):
            self.proxy = ServerProxyModel(**raw_proxy)


@dataclass
class ServerModelCreate:
    name: str
    description: str
    ip: str
    port: int
    user: str
    private_key_uuid: str
    is_build_server: bool
    instant_validate: bool
    proxy_type: str = _COOLIFY_DEFAULT_PROXY
