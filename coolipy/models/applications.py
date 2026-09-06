"""Application models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.enums import BuildPack, Redirect
from coolipy.models.base import CoolipyBaseModel


class DockerComposeDomain(CoolipyBaseModel):
    """A per-service domain mapping for docker-compose applications."""

    name: str | None = None
    domain: str | None = None
    redirect: Redirect | None = None


class ApplicationSetting(CoolipyBaseModel):
    """Application settings returned as part of an application model."""

    is_static: bool | None = None
    is_git_submodules_enabled: bool | None = None
    is_git_lfs_enabled: bool | None = None
    is_auto_deploy_enabled: bool | None = None
    is_force_https_enabled: bool | None = None
    is_debug_enabled: bool | None = None
    is_preview_deployments_enabled: bool | None = None
    is_log_drain_enabled: bool | None = None
    is_gpu_enabled: bool | None = None
    gpu_driver: str | None = None
    gpu_count: str | None = None
    gpu_device_ids: str | None = None
    gpu_options: str | None = None
    is_include_timestamps: bool | None = None
    is_swarm_only_worker_nodes: bool | None = None
    is_raw_compose_deployment_enabled: bool | None = None
    is_build_server_enabled: bool | None = None
    is_consistent_container_name_enabled: bool | None = None
    is_gzip_enabled: bool | None = None
    is_stripprefix_enabled: bool | None = None
    connect_to_docker_network: bool | None = None
    custom_internal_name: str | None = None
    is_container_label_escape_enabled: bool | None = None
    is_env_sorting_enabled: bool | None = None
    is_container_label_readonly_enabled: bool | None = None
    is_preserve_repository_enabled: bool | None = None
    disable_build_cache: bool | None = None
    is_spa: bool | None = None
    is_git_shallow_clone_enabled: bool | None = None
    is_pr_deployments_public_enabled: bool | None = None
    use_build_secrets: bool | None = None
    inject_build_args_to_dockerfile: bool | None = None
    include_source_commit_in_build: bool | None = None
    docker_images_to_keep: int | None = None
    stop_grace_period: int | None = None


class ApplicationModel(CoolipyBaseModel):
    """An application as returned by the API."""

    id: int | None = None
    description: str | None = None
    repository_project_id: int | None = None
    uuid: str | None = None
    name: str | None = None
    fqdn: str | None = None
    noindex_domains: list[str] | None = None
    config_hash: str | None = None
    git_repository: str | None = None
    git_branch: str | None = None
    git_commit_sha: str | None = None
    git_full_url: str | None = None
    docker_registry_image_name: str | None = None
    docker_registry_image_tag: str | None = None
    build_pack: str | None = None
    static_image: str | None = None
    install_command: str | None = None
    build_command: str | None = None
    start_command: str | None = None
    ports_exposes: str | None = None
    ports_mappings: str | None = None
    custom_network_aliases: str | None = None
    base_directory: str | None = None
    publish_directory: str | None = None
    health_check_enabled: bool | None = None
    health_check_path: str | None = None
    health_check_port: str | None = None
    health_check_host: str | None = None
    health_check_method: str | None = None
    health_check_return_code: int | None = None
    health_check_scheme: str | None = None
    health_check_response_text: str | None = None
    health_check_interval: int | None = None
    health_check_timeout: int | None = None
    health_check_retries: int | None = None
    health_check_start_period: int | None = None
    health_check_type: str | None = None
    health_check_command: str | None = None
    limits_memory: str | None = None
    limits_memory_swap: str | None = None
    limits_memory_swappiness: int | None = None
    limits_memory_reservation: str | None = None
    limits_cpus: str | None = None
    limits_cpuset: str | None = None
    limits_cpu_shares: int | None = None
    status: str | None = None
    preview_url_template: str | None = None
    max_restart_count: int | None = None
    destination_type: str | None = None
    destination_id: int | None = None
    source_id: int | None = None
    private_key_id: int | None = None
    environment_id: int | None = None
    dockerfile: str | None = None
    dockerfile_location: str | None = None
    custom_labels: str | None = None
    dockerfile_target_build: str | None = None
    manual_webhook_secret_github: str | None = None
    manual_webhook_secret_gitlab: str | None = None
    manual_webhook_secret_bitbucket: str | None = None
    manual_webhook_secret_gitea: str | None = None
    docker_compose_location: str | None = None
    docker_compose: str | None = None
    docker_compose_raw: str | None = None
    docker_compose_domains: str | None = None
    docker_compose_custom_start_command: str | None = None
    docker_compose_custom_build_command: str | None = None
    swarm_replicas: int | None = None
    swarm_placement_constraints: str | None = None
    custom_docker_run_options: str | None = None
    post_deployment_command: str | None = None
    post_deployment_command_container: str | None = None
    pre_deployment_command: str | None = None
    pre_deployment_command_container: str | None = None
    watch_paths: str | None = None
    custom_healthcheck_found: bool | None = None
    redirect: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    compose_parsing_version: str | None = None
    custom_nginx_configuration: str | None = None
    is_http_basic_auth_enabled: bool | None = None
    http_basic_auth_username: str | None = None
    http_basic_auth_password: str | None = None
    settings: ApplicationSetting | None = None


class ApplicationBaseModel(CoolipyBaseModel):
    """Shared fields for application create/update request bodies."""

    project_uuid: str | None = None
    server_uuid: str | None = None
    environment_name: str | None = None
    environment_uuid: str | None = None
    git_repository: str | None = None
    git_branch: str | None = None
    build_pack: BuildPack | None = None
    ports_exposes: str | None = None
    destination_uuid: str | None = None
    name: str | None = None
    description: str | None = None
    domains: str | None = None
    noindex_domains: list[str] | None = None
    git_commit_sha: str | None = None
    docker_registry_image_name: str | None = None
    docker_registry_image_tag: str | None = None
    is_static: bool | None = None
    is_spa: bool | None = None
    is_auto_deploy_enabled: bool | None = None
    is_force_https_enabled: bool | None = None
    is_preview_deployments_enabled: bool | None = None
    static_image: str | None = None
    install_command: str | None = None
    build_command: str | None = None
    start_command: str | None = None
    ports_mappings: str | None = None
    base_directory: str | None = None
    publish_directory: str | None = None
    health_check_enabled: bool | None = None
    health_check_path: str | None = None
    health_check_port: str | None = None
    health_check_host: str | None = None
    health_check_method: str | None = None
    health_check_return_code: int | None = None
    health_check_scheme: str | None = None
    health_check_response_text: str | None = None
    health_check_interval: int | None = None
    health_check_timeout: int | None = None
    health_check_retries: int | None = None
    health_check_start_period: int | None = None
    limits_memory: str | None = None
    limits_memory_swap: str | None = None
    limits_memory_swappiness: int | None = None
    limits_memory_reservation: str | None = None
    limits_cpus: str | None = None
    limits_cpuset: str | None = None
    limits_cpu_shares: int | None = None
    custom_labels: str | None = None
    custom_docker_run_options: str | None = None
    post_deployment_command: str | None = None
    post_deployment_command_container: str | None = None
    pre_deployment_command: str | None = None
    pre_deployment_command_container: str | None = None
    manual_webhook_secret_github: str | None = None
    manual_webhook_secret_gitlab: str | None = None
    manual_webhook_secret_bitbucket: str | None = None
    manual_webhook_secret_gitea: str | None = None
    redirect: Redirect | None = None
    instant_deploy: bool | None = None
    dockerfile: str | None = None
    dockerfile_location: str | None = None
    docker_compose_location: str | None = None
    docker_compose_custom_start_command: str | None = None
    docker_compose_custom_build_command: str | None = None
    docker_compose_domains: list[DockerComposeDomain] | None = None
    watch_paths: str | None = None
    use_build_server: bool | None = None
    use_build_secrets: bool | None = None
    is_git_submodules_enabled: bool | None = None
    is_git_lfs_enabled: bool | None = None
    is_git_shallow_clone_enabled: bool | None = None
    disable_build_cache: bool | None = None
    inject_build_args_to_dockerfile: bool | None = None
    include_source_commit_in_build: bool | None = None
    is_env_sorting_enabled: bool | None = None
    is_pr_deployments_public_enabled: bool | None = None
    stop_grace_period: int | None = None
    docker_images_to_keep: int | None = None
    is_gzip_enabled: bool | None = None
    is_stripprefix_enabled: bool | None = None
    is_raw_compose_deployment_enabled: bool | None = None
    is_log_drain_enabled: bool | None = None
    is_gpu_enabled: bool | None = None
    gpu_driver: str | None = None
    gpu_count: str | None = None
    gpu_device_ids: str | None = None
    gpu_options: str | None = None
    is_consistent_container_name_enabled: bool | None = None
    custom_internal_name: str | None = None
    preview_url_template: str | None = None
    max_restart_count: int | None = None
    is_http_basic_auth_enabled: bool | None = None
    http_basic_auth_username: str | None = None
    http_basic_auth_password: str | None = None
    connect_to_docker_network: bool | None = None
    force_domain_override: bool | None = None
    autogenerate_domain: bool | None = None
    is_container_label_escape_enabled: bool | None = None
    tags: list[str] | None = None
    is_preserve_repository_enabled: bool | None = None
    github_app_uuid: str | None = None
    private_key_uuid: str | None = None


class ApplicationUpdateModel(ApplicationBaseModel):
    """Body for updating an application."""


class ApplicationPublicModelCreate(ApplicationBaseModel):
    """Create an application from a public git repository."""


class ApplicationPrivateGHModelCreate(ApplicationBaseModel):
    """Create an application from a private repository via a GitHub App."""


class ApplicationPrivateDeployKeyModelCreate(ApplicationBaseModel):
    """Create an application from a private repository via a deploy key."""


class ApplicationDockerfileModelCreate(ApplicationBaseModel):
    """Create an application from a Dockerfile."""


class ApplicationDockerImageModelCreate(ApplicationBaseModel):
    """Create an application from a prebuilt Docker image."""
