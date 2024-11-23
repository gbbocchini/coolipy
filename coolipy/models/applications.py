from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union

from coolipy.constants import COOLIFY_BUILD_PACKS, COOLIFY_REDIRECT
from coolipy.models.base import CoolipyBaseModel
from coolipy.models.databases import DestinationModel


@dataclass
class ServiceApplicationModel(CoolipyBaseModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    human_name: Optional[str] = None
    description: Optional[str] = None
    fqdn: Optional[str] = None
    ports: Optional[List[str]] = None
    exposes: Optional[str] = None
    status: Optional[str] = None
    service_id: Optional[int] = None
    exclude_from_status: Optional[bool] = None
    required_fqdn: Optional[bool] = None
    image: Optional[str] = None
    is_log_drain_enabled: Optional[bool] = None
    is_include_timestamps: Optional[bool] = None
    deleted_at: Optional[Union[str, datetime]] = None
    is_gzip_enabled: Optional[bool] = None
    is_stripprefix_enabled: Optional[bool] = None
    last_online_at: Optional[Union[str, datetime]] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None


@dataclass
class ApplicationBaseModel:
    uuid: Optional[str] = None
    name: Optional[str] = None
    domains: Optional[List[str]] = field(default_factory=list)
    description: Optional[str] = None
    git_repository: Optional[str] = None
    git_branch: Optional[str] = None
    build_pack: Optional[COOLIFY_BUILD_PACKS] = None
    docker_registry_image_name: Optional[str] = None
    docker_registry_image_tag: Optional[str] = None
    static_image: Optional[str] = None
    install_command: Optional[str] = None
    build_command: Optional[str] = None
    start_command: Optional[str] = None
    base_directory: Optional[str] = None
    publish_directory: Optional[str] = None
    health_check_enabled: Optional[bool] = None
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
    custom_labels: Optional[str] = None
    custom_docker_run_options: Optional[str] = None
    post_deployment_command: Optional[str] = None
    post_deployment_command_container: Optional[str] = None
    pre_deployment_command: Optional[str] = None
    pre_deployment_command_container: Optional[str] = None
    manual_webhook_secret_github: Optional[str] = None
    manual_webhook_secret_gitlab: Optional[str] = None
    manual_webhook_secret_bitbucket: Optional[str] = None
    manual_webhook_secret_gitea: Optional[str] = None
    dockerfile: Optional[str] = None
    docker_compose_location: Optional[str] = None
    docker_compose_raw: Optional[str] = None
    docker_compose_custom_start_command: Optional[str] = None
    docker_compose_custom_build_command: Optional[str] = None
    docker_compose_domains: Optional[List[str]] = None
    watch_paths: Optional[List[str]] = None


@dataclass
class ApplicationModel(ApplicationBaseModel, CoolipyBaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    additional_servers: Optional[List] = None
    base_directory: Optional[str] = None
    build_command: Optional[str] = None
    build_pack: Optional[COOLIFY_BUILD_PACKS] = None
    compose_parsing_version: Optional[str] = None
    config_hash: Optional[str] = None
    custom_docker_run_options: Optional[str] = None
    custom_healthcheck_found: Optional[bool] = None
    custom_labels: Optional[str] = None
    custom_nginx_configuration: Optional[str] = None
    deleted_at: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[DestinationModel] = None
    destination_id: Optional[int] = None
    destination_type: Optional[str] = None
    docker_compose: Optional[str] = None
    docker_compose_custom_build_command: Optional[str] = None
    docker_compose_custom_start_command: Optional[str] = None
    docker_compose_domains: Optional[List] = None
    docker_compose_location: Optional[str] = None
    docker_compose_raw: Optional[str] = None
    docker_registry_image_name: Optional[str] = None
    docker_registry_image_tag: Optional[str] = None
    dockerfile: Optional[str] = None
    dockerfile_location: Optional[str] = None
    dockerfile_target_build: Optional[str] = None
    environment_id: Optional[int] = None
    fqdn: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit_sha: Optional[str] = None
    git_full_url: Optional[str] = None
    git_repository: Optional[str] = None
    health_check_enabled: Optional[bool] = None
    health_check_host: Optional[str] = None
    health_check_interval: Optional[int] = None
    health_check_method: Optional[str] = None
    health_check_path: Optional[str] = None
    health_check_port: Optional[int] = None
    health_check_response_text: Optional[str] = None
    health_check_retries: Optional[int] = None
    health_check_return_code: Optional[int] = None
    health_check_scheme: Optional[str] = None
    health_check_start_period: Optional[int] = None
    health_check_timeout: Optional[int] = None
    install_command: Optional[str] = None
    laravel_through_key: Optional[int] = None
    last_online_at: Optional[str] = None
    limits_cpu_shares: Optional[int] = None
    limits_cpus: Optional[str] = None
    limits_cpuset: Optional[str] = None
    limits_memory: Optional[str] = None
    limits_memory_reservation: Optional[str] = None
    limits_memory_swap: Optional[str] = None
    limits_memory_swappiness: Optional[int] = None
    manual_webhook_secret_bitbucket: Optional[str] = None
    manual_webhook_secret_gitea: Optional[str] = None
    manual_webhook_secret_github: Optional[str] = None
    manual_webhook_secret_gitlab: Optional[str] = None
    ports_exposes: Optional[str] = None
    ports_mappings: Optional[List] = field(default_factory=list)
    post_deployment_command: Optional[str] = None
    post_deployment_command_container: Optional[str] = None
    pre_deployment_command: Optional[str] = None
    pre_deployment_command_container: Optional[str] = None
    preview_url_template: Optional[str] = None
    private_key_id: Optional[str] = None
    publish_directory: Optional[str] = None
    redirect: Optional[str] = None
    repository_project_id: Optional[str] = None
    server_status: Optional[bool] = None
    source_id: Optional[int] = None
    source_type: Optional[str] = None
    start_command: Optional[str] = None
    static_image: Optional[str] = None
    status: Optional[str] = None
    swarm_placement_constraints: Optional[str] = None
    swarm_replicas: Optional[int] = None
    watch_paths: Optional[List] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None

    def _adjust_nested(self):
        raw_server = self.destination
        if isinstance(raw_server, dict) and raw_server:
            self.destination = DestinationModel(**raw_server).pythonify()


@dataclass
class ApplicationPublicModelCreate:
    name: str
    project_uuid: str
    server_uuid: str
    environment_name: str
    ports_exposes: str
    instant_deploy: bool

@dataclass
class ApplicationPublicGHModelCreate(ApplicationPublicModelCreate):
    github_app_uuid: int
    git_repository: str
    git_branch: str
    build_pack: COOLIFY_BUILD_PACKS


@dataclass
class ApplicationPrivateGHModelCreate(ApplicationPublicModelCreate):
    github_app_uuid: int
    git_repository: str
    git_branch: str
    build_pack: COOLIFY_BUILD_PACKS

@dataclass
class ApplicationPublicPrivatePvtKeyGHModelCreate(ApplicationPublicModelCreate):
    private_key_uuid: str

@dataclass
class ApplicationDockerfileModelCreate(ApplicationPublicModelCreate):
    dockerfile: str

@dataclass
class ApplicationDockerImageModelCreate(ApplicationPublicModelCreate):
    docker_registry_image_name: str
    docker_registry_image_tag: Optional[str] = ""

@dataclass
class ApplicationDockerComposeModelCreate(ApplicationPublicModelCreate):
    docker_compose_raw: str


APPLICATION_MODELS_URL_CREATE_MAP = {
    ApplicationPublicGHModelCreate: "public",
    ApplicationPrivateGHModelCreate: "private-github-app",
    ApplicationPublicPrivatePvtKeyGHModelCreate: "private-deploy-key",
    ApplicationDockerfileModelCreate: "dockerfile",
    ApplicationDockerImageModelCreate: "dockerimage",
    ApplicationDockerComposeModelCreate: "dockercompose",
}
