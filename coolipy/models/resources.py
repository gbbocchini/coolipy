from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union

from coolipy.models.base import CoolipyBaseModel
from coolipy.models.databases import DestinationModel
from coolipy.models.environs import EnvironmentsModel
from coolipy.models.servers import ServerModel
from coolipy.models.service import ServiceModel


@dataclass
class ResourceModel(CoolipyBaseModel):
    """
    Coolify Resource data model.
    """

    id: Optional[int] = None
    repository_project_id: Optional[int] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    fqdn: Optional[str] = None
    config_hash: Optional[str] = None
    git_repository: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit_sha: Optional[str] = None
    git_full_url: Optional[str] = None
    docker_registry_image_name: Optional[str] = None
    docker_registry_image_tag: Optional[str] = None
    build_pack: Optional[str] = None
    static_image: Optional[str] = None
    install_command: Optional[str] = None
    build_command: Optional[str] = None
    start_command: Optional[str] = None
    ports_exposes: Optional[str] = None
    ports_mappings: Optional[str] = None
    base_directory: Optional[str] = None
    publish_directory: Optional[str] = None
    health_check_path: Optional[str] = None
    health_check_port: Optional[int] = None
    health_check_host: Optional[str] = None
    health_check_method: Optional[str] = None
    health_check_return_code: Optional[int] = None
    health_check_scheme: Optional[str] = None
    health_check_response_text: Optional[str] = None
    health_check_interval: Optional[int] = None
    health_check_timeout: Optional[int] = None
    health_check_retries: Optional[int] = None
    health_check_start_period: Optional[int] = None
    limits_memory: Optional[str] = None
    limits_memory_swap: Optional[str] = None
    limits_memory_swappiness: Optional[int] = None
    limits_memory_reservation: Optional[str] = None
    limits_cpus: Optional[str] = None
    limits_cpuset: Optional[str] = None
    limits_cpu_shares: Optional[int] = None
    status: Optional[str] = None
    preview_url_template: Optional[str] = None
    destination_type: Optional[str] = None
    destination_id: Optional[int] = None
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    private_key_id: Optional[int] = None
    environment_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    dockerfile: Optional[str] = None
    health_check_enabled: Optional[bool] = None
    dockerfile_location: Optional[str] = None
    custom_labels: Optional[str] = None
    dockerfile_target_build: Optional[str] = None
    manual_webhook_secret_github: Optional[str] = None
    manual_webhook_secret_gitlab: Optional[str] = None
    docker_compose_location: Optional[str] = None
    docker_compose: Optional[str] = None
    docker_compose_raw: Optional[str] = None
    docker_compose_domains: Optional[str] = None
    deleted_at: Optional[str] = None
    docker_compose_custom_start_command: Optional[str] = None
    docker_compose_custom_build_command: Optional[str] = None
    swarm_replicas: Optional[int] = None
    swarm_placement_constraints: Optional[str] = None
    manual_webhook_secret_bitbucket: Optional[str] = None
    custom_docker_run_options: Optional[str] = None
    post_deployment_command: Optional[str] = None
    post_deployment_command_container: Optional[str] = None
    pre_deployment_command: Optional[str] = None
    pre_deployment_command_container: Optional[str] = None
    watch_paths: Optional[str] = None
    custom_healthcheck_found: Optional[bool] = None
    manual_webhook_secret_gitea: Optional[str] = None
    redirect: Optional[str] = None
    compose_parsing_version: Optional[str] = None
    last_online_at: Optional[str] = None
    custom_nginx_configuration: Optional[str] = None
    laravel_through_key: Optional[int] = None
    server_status: Optional[bool] = None
    additional_servers: Optional[List[ServerModel]] = None
    destination: Optional[DestinationModel] = None
    service_type: Optional[str] = None
    connect_to_docker_network: Optional[bool] = None
    is_container_label_escape_enabled: Optional[bool] = None
    server: Optional[ServerModel] = None
    services: Optional[ServiceModel] = None
    deployment_environment: Optional[EnvironmentsModel] = None
    type: Optional[str] = None
    server_id: Optional[str] = None
    mongo_conf: Optional[str] = None
    mongo_initdb_root_username: Optional[str] = None
    mongo_initdb_root_password: Optional[str] = None
    mongo_initdb_database: Optional[str] = None
    image: Optional[str] = None
    is_public: Optional[str] = None
    public_port: Optional[int] = None
    started_at: Optional[str] = None
    is_log_drain_enabled: Optional[str] = None
    is_include_timestamps: Optional[bool] = None
    internal_db_url: Optional[str] = None
    external_db_url: Optional[str] = None
    database_type: Optional[str] = None

    def _adjust_nested(self):
        raw_server = self.server
        raw_dest = self.destination
        raw_env = self.deployment_environment

        if isinstance(raw_server, dict) and raw_server:
            self.server = ServerModel(**raw_server).pythonify()

        if isinstance(raw_dest, dict) and raw_dest:
            self.destination = DestinationModel(**raw_dest).pythonify()

        if isinstance(raw_env, dict) and raw_env:
            self.deployment_environment = EnvironmentsModel(**raw_env).pythonify()
