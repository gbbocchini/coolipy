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
- Manage Coolify projects, servers, applications, deployments and more (everything the Coolify App offers)ç
- Infra as code;
- 1 dependency: requests>=2.32.3;
- Datamodels for all endpoints;
- Datamodels specific for creation with only the required fields;
- All responses come from Datamodels;

TO DO:

- Async support.



# Quick Start Guide

- Import and Initialize
```python
from coolipy import Coolipy

coolify_client = Coolipy(
    coolify_api_key="your_coolify_api_key",
    coolify_endpoint="your_coolify_instance_address",
)
```

## Example Usage

- Get Project Information
```python
my_project = coolify_client.projects.get(project_uuid="your_project_uuid")
```

- Create a Service
```python
from coolipy.models.service import ServiceModelCreate

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


- List Servers
```python
servers = coolify_client.servers.list()
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

