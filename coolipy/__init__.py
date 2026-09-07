"""The (un)official, fully-typed Python client for the [Coolify](https://coolify.io) API.

`coolipy` wraps the complete token-gated Coolify REST API in a single package with
two clients — a synchronous :class:`Coolipy` and an asynchronous :class:`AsyncCoolipy` —
both backed by a dependency-injected [httpx](https://github.com/encode/httpx) transport.
Every request body and every response body is a [pydantic](https://docs.pydantic.dev/) model:
there is no raw JSON to build or parse by hand.

## Install

```bash
pip install coolipy
# or
uv add coolipy
```

Requires **Python 3.10+**.

## Quick start

Synchronous:

```python
from coolipy import Coolipy

with Coolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    print(client.health().data)   # 'OK'
    print(client.version().data)  # '4.3.17'
```

Asynchronous:

```python
import asyncio

from coolipy import AsyncCoolipy

async def main() -> None:
    async with AsyncCoolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
        resp = await client.projects.list()
        print(resp.data)

asyncio.run(main())
```

## Example — deploy an application

```python
from coolipy import Coolipy
from coolipy.models.applications import ApplicationDockerImageModelCreate

app = ApplicationDockerImageModelCreate(
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    docker_registry_image_name="nginx",
    docker_registry_image_tag="latest",
    name="my-nginx",
    ports_exposes="80",
)

with Coolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    resp = client.applications.create(app)
    print(resp.data)  # UUIDResponse(uuid='6zacuhbss0pnxtjihzmxolds')
```

## Example — provision a database

```python
from coolipy import Coolipy
from coolipy.models.databases import PostgreSQLModelCreate

db = PostgreSQLModelCreate(
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    postgres_user="dbuser",
    postgres_password="password",
    postgres_db="mydatabase",
    name="My PostgreSQL DB",
)

with Coolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    resp = client.databases.create(db)
```

## Resources

Each resource is a sub-client on the client instance:

| Sub-client | What it manages |
| --- | --- |
| `client.projects` | Projects and environments |
| `client.servers` | Servers, destinations, resources, validation |
| `client.applications` | Applications (git / docker image / dockerfile), envs, storages, tags, scheduled tasks |
| `client.databases` | PostgreSQL, MySQL, MariaDB, MongoDB, Redis, ClickHouse, Dragonfly, KeyDB |
| `client.services` | Docker Compose services (incl. per-service apps and databases) |
| `client.deployments` | Deployments and `deploy` |
| `client.teams` | Teams, members, shared environment variables |
| `client.tags` | Global tags |
| `client.s3_storages` | S3 storage backends |
| `client.security` | Private keys |

System endpoints live on the client directly: `version()`, `health()`, `enable_api()`,
`disable_api()`, `enable_mcp()`, `disable_mcp()`.

## Responses

Every method returns a `CoolipyAPIResponse[T]` with three fields: `status_code`, validated
`data`, and `headers`. Non-2xx responses raise `CoolipyHTTPError`, which carries the API's
error details — see `CoolipyError`, `CoolipyConfigError` and `CoolipyValidationError` for the
client-side failures.

See the [full guide](https://coolipydocs.gabrielbocchini.com.br/llms-full.txt) for
copy-paste examples of every resource, in both sync and async flavours.
"""

from __future__ import annotations

from coolipy._response import CoolipyAPIResponse
from coolipy.async_client import AsyncCoolipy
from coolipy.client import Coolipy
from coolipy.exceptions import (
    CoolipyConfigError,
    CoolipyError,
    CoolipyHTTPError,
    CoolipyValidationError,
)
from coolipy.models.base import CoolipyBaseModel

__version__ = "1.0.0"

__all__ = [
    "AsyncCoolipy",
    "Coolipy",
    "CoolipyAPIResponse",
    "CoolipyBaseModel",
    "CoolipyConfigError",
    "CoolipyError",
    "CoolipyHTTPError",
    "CoolipyValidationError",
    "__version__",
]
