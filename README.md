# Coolipy

**The first (un)official Python client for the [Coolify](https://coolify.io/).**
Coolipy simplifies programmatically interacting with Coolify by providing wrappers around [Coolify API](https://coolify.io/docs/api), enabling you to manage projects, deployments, servers, services, and more with python scripts.

- Lib docs: https://coolipydocs.gabrielbocchini.com.br/
- Coolify API docs: https://coolify.io/docs/api

## Installation

Install Coolipy using pip:

```bash
pip install coolipy
```

## Features
- Manage Coolify projects, servers, applications, deployments and more (everything the Coolify App offers);
- Infra as code;
- 1 dependency: requests>=2.32.3;
- Datamodels for all endpoints;
- Datamodels specific for creation with only the required fields;
- All responses come from Datamodels;

TO DO:

- Async support.


## Lib Assets

- `coolipy.models`: hold all data models used to hold retrieved data. Create methods use models names following the pattern: `<service>ModelCreate`;
- `coolipy.services`: methods used to interact with the Coolify API.
-


# Quick Start Guide/Examples

- Import and Initialize
```python
from coolipy import Coolipy

coolify_client = Coolipy(
    coolify_api_key="your_coolify_api_key",
    coolify_endpoint="your_coolify_instance_address",
)
```

## Example Usage

- Create a Project
```python
my_project = coolify_client.projects.create(project_name="MyProject", project_description="This is MyProject description")
```

The response will be a [CoolipyAPIResponse](https://github.com/gbbocchini/coolipy/blob/main/coolipy/models/coolify_api_response.py) containing the Coolify api response code and `data`, in this case, will be a [ProjectsModel](https://github.com/gbbocchini/coolipy/blob/main/coolipy/models/projects.py).

```bash
>print(my_project)

CoolifyAPIResponse(
    status_code=201,
    data=ProjectsModel(
        name=MyProject,
        description=This is MyProject description,
        id=None,
        uuid='b84skk8c4owskskogko40s44',
        default_environment=None,
        environments=[],
        team_id=None,
        created_at=None,
        updated_at=None
    )
)
```

- List Servers
```python
servers = coolify_client.servers.list()

>print(servers)

CoolifyAPIResponse(
    status_code=200,
    data=[
        ServerModel(
            id=None,
            description="This is the server where Coolify is running on. Don't delete this!",
            name='localhost', ip='host.docker.internal',
            port=22,
            user='root',
            private_key_id=None,
            uuid='gwogk4ssckgw8gwokcswww4o',
            team_id=None,
            sentinel_updated_at=None,
            reated_at=None,
            updated_at=None,
            deleted_at=None,
            high_disk_usage_notification_sent=False,
            log_drain_notification_sent=False,
            swarm_cluster=False,
            validation_logs=None,
            unreachable_count=None,
            unreachable_notification_sent=False,
            proxy=ServerProxyModel(
                type='traefik',
                status=None,
                last_saved_settings=None,
                last_applied_settings=None,
                force_stop=None,
                redirect_enabled=True
            ),
            settings=ServerSettingsModel(
                id=1,
                concurrent_builds=2,
                delete_unused_networks=False,
                delete_unused_volumes=False,
                docker_cleanup_frequency='0 0 * * *',
                docker_cleanup_threshold=80,
                dynamic_timeout=3600,
                force_disabled=False,
                force_docker_cleanup=True,
                generate_exact_labels=False,
                is_build_server=False,
                is_cloudflare_tunnel=False,
                is_jump_server=False,
                is_logdrain_axiom_enabled=False,
                is_logdrain_custom_enabled=False,
                is_logdrain_highlight_enabled=False,
                is_logdrain_newrelic_enabled=False,
                is_metrics_enabled=False,
                is_reachable=True,
                is_sentinel_debug_enabled=False,
                is_sentinel_enabled=False,
                is_swarm_manager=False,
                is_swarm_worker=False,
                is_usable=True,
                sentinel_custom_url='http://host.docker.internal:8000',
                sentinel_metrics_history_days=7,
                sentinel_metrics_refresh_rate_seconds=10,
                sentinel_push_interval_seconds=60,
                sentinel_token='==',
                server_disk_usage_notification_threshold=80,
                server_id=0, server_timezone='UTC',
                 created_at=datetime.datetime(2025, 1, 13, 19, 6, 12, tzinfo=datetime.timezone.utc),
                 updated_at=datetime.datetime(2025, 1, 13, 19, 7, 19, tzinfo=datetime.timezone.utc),
                 logdrain_axiom_api_key=None,
                 logdrain_axiom_dataset_name=None,
                 logdrain_custom_config=None,
                 logdrain_custom_config_parser=None,
                 logdrain_highlight_project_id=None,
                 logdrain_newrelic_base_uri=None,
                 logdrain_newrelic_license_key=None,
                 wildcard_domain=None
            ),
            is_reachable=True,
            is_usable=True
        )
    ]
)
```

- Create a Service
```python
from coolipy.models.service import ServiceModelCreate
from coolipy.constants import COOLIFY_SERVICE_TYPES

service_data = ServiceModelCreate(
    type=COOLIFY_SERVICE_TYPES.glance,
    name="Example Service",
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    destination_uuid="your_destination_uuid",
    instant_deploy=True,
    environment_name="production"
)
new_service = coolify_client.services.create(service_data)
```

- Create a DB:
```python
from coolipy.models.databases import PostgreSQLModelCreate

postgres_db = PostgreSQLModelCreate(
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    is_public=False,
    limits_cpu_shares=0,
    limits_cpus=0,
    limits_cpuset=0,
    limits_memory=0,
    limits_memory_reservation=0,
    limits_memory_swap=0,
    limits_memory_swappiness=0,
    instant_deploy=True,
    postgres_user="dbuser",
    postgres_password="password",
    postgres_db="mydatabase",
    name="My PostgreSQL DB",
    postgres_conf="LQ==",  # Example config
    postgres_host_auth_method="-",
    postgres_initdb_args="-"
)

my_database = coolify_client.databases.create(database_model_create=postgres_db)
```

- Create an App
```python
from coolipy.models.applications import ApplicationPrivateGHModelCreate

app_data = ApplicationPrivateGHModelCreate(
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    ports_exposes="8080",
    github_app_uuid="your_github_app_uuid",
    git_repository="your_github_repo",
    git_branch="main",
    build_pack=COOLIFY_BUILD_PACKS.dockerfile,
    instant_deploy=True,
    name="MyApp"
)

new_app = coolify_client.applications.create(app_data)
```

# Contributing

- Before opening a pull request or issue, take some time to understand if the issue should be treated at
this client level OR the Coolify REST API;
- Create a fork of this repo and then submit a pull request;
- Respect Python PEPs and type inference;
- Test your code or changes introduced and deliver unit tests on the PR;
- No breaking changes unless if necessary due Coolipy REST API change (please provide Coolipy PR/commits of the change).


# License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.
