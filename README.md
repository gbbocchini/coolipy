# Coolipy

**The (un)official Python client for [Coolify](https://coolify.io/).**

Coolipy wraps the [Coolify REST API](https://coolify.io/docs/api) with typed models and ships **synchronous** and **asynchronous** clients in a single package.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![CI](https://github.com/gbbocchini/coolipy/actions/workflows/ci.yml/badge.svg)](https://github.com/gbbocchini/coolipy/actions/workflows/ci.yml)

- Lib docs: https://coolipydocs.gabrielbocchini.com.br/
- Coolify API docs: https://coolify.io/docs/api

## Installation

```bash
pip install coolipy
# or
uv add coolipy
```

Requires **Python 3.10+**. Runtime dependencies: [`httpx`](https://github.com/encode/httpx) and [`pydantic`](https://docs.pydantic.dev/).

## Features

- Synchronous **and** asynchronous clients in one package.
- Typed request and response models (pydantic) for every endpoint.
- A single `CoolipyAPIResponse[T]` envelope: `status_code`, validated `data`, and `headers`.
- Typed exceptions that carry the API's validation errors.
- Built on `httpx` with a dependency-injected transport (easy to mock in tests).

## Quick start

### Synchronous

```python
from coolipy import Coolipy

client = Coolipy(
    coolify_api_key="YOUR_API_TOKEN",
    coolify_endpoint="your-coolify-instance.com",
    http_protocol="https",
    coolify_port=8000,
)

resp = client.version()
print(resp.status_code)  # 200
print(resp.data)         # e.g. "v4.0.0"

client.close()
```

Use it as a context manager to close automatically:

```python
with Coolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    print(client.health().data)  # "OK"
```

### Asynchronous

```python
import asyncio

from coolipy import AsyncCoolipy

async def main() -> None:
    async with AsyncCoolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
        resp = await client.version()
        print(resp.data)

asyncio.run(main())
```

## Responses

Every method returns a [`CoolipyAPIResponse`](coolipy/_response.py) with three fields:

| Field | Type | Description |
| --- | --- | --- |
| `status_code` | `int` | HTTP status code. |
| `data` | `T` | Parsed body, validated against a model when one exists. |
| `headers` | `dict[str, str]` | Response headers. |

```python
resp = client.enable_api()
print(resp.data)          # SystemMessage(message='API enabled.')
print(resp.data.message)  # 'API enabled.'
```

## Errors

Non-2xx responses raise [`CoolipyHTTPError`](coolipy/exceptions.py), which carries the API's error details:

```python
from coolipy.exceptions import CoolipyHTTPError

try:
    client.version()
except CoolipyHTTPError as exc:
    print(exc.status_code)  # e.g. 401
    print(exc.message)      # e.g. "Unauthenticated."
    print(exc.errors)       # field-level messages for 422 responses
```

`CoolipyError` is the base class; `CoolipyConfigError` and `CoolipyValidationError` cover client-side problems.

## Models & enums

Every request and response body is a [`pydantic`](https://docs.pydantic.dev/) model deriving from [`CoolipyBaseModel`](coolipy/models/base.py). Enums mirror the API's string-constrained fields:

```python
from coolipy.enums import BuildPack, ProxyType, ServiceType

BuildPack.RAILPACK.value  # "railpack"
ProxyType.NONE.value      # "none"
```

## Usage examples

Each resource is a sub-client on `Coolipy`/`AsyncCoolipy` (`client.projects`, `client.servers`, `client.applications`, …). Requests take a typed model; responses come back as a `CoolipyAPIResponse` with a validated model in `.data`.

### Projects

```python
from coolipy.models.projects import ProjectCreateModel

resp = client.projects.create(
    ProjectCreateModel(name="My Project", description="Created with Coolipy")
)
print(resp.status_code)  # 201
print(resp.data)         # UUIDResponse(uuid='og888os')

resp = client.projects.list()
print(resp.data)
# [
#   ProjectModel(id=1, uuid='og888os', name='My Project', description='Created with Coolipy'),
# ]
```

### Servers

```python
resp = client.servers.list()
for server in resp.data:
    print(server.name, server.ip, server.proxy_type)
```

### Applications, databases, and services

```python
resp = client.applications.list()
print([app.name for app in resp.data])

resp = client.databases.list()
print([db.name for db in resp.data])

resp = client.services.list()
print([svc.name for svc in resp.data])
```

### Creating an application

```python
from coolipy.enums import BuildPack
from coolipy.models.applications import ApplicationPublicModelCreate

app = ApplicationPublicModelCreate(
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    git_repository="https://github.com/your/repo",
    git_branch="main",
    build_pack=BuildPack.NIXPACKS,
    name="My App",
    instant_deploy=True,
)
resp = client.applications.create(app)
print(resp.data)  # UUIDResponse(uuid='...')
```

### Async

```python
async with AsyncCoolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    resp = await client.projects.list()
    print(resp.data)
```

## Configuration

Both clients take the same arguments:

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `coolify_api_key` | `str` | — | Bearer token for the Coolify API. |
| `coolify_endpoint` | `str` | — | Hostname/IP of the Coolify instance. |
| `coolify_port` | `int` | `8000` | Port (ignored when `omit_port=True`). |
| `omit_port` | `bool` | `False` | Build the base URL without a port. |
| `http_protocol` | `str` | `"http"` | `"http"` or `"https"`. |
| `timeout` | `float` | `30.0` | Request timeout in seconds. |

## Status

Coolipy **1.0.0** covers the full token-gated Coolify API surface — applications, databases, services, servers, projects, environments, teams, deployments, tags, S3 storages, private keys, shared envs, and the system endpoints — in both sync and async flavours. Real-world smoke tests in [`tests/smoke/`](tests/smoke/) exercise these against a live instance (skipped unless credentials are provided).

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy coolipy
```

Run the real-world smoke tests against a live instance (no secrets committed — provided via env vars):

```bash
COOLIPY_API_KEY=... COOLIPY_ENDPOINT=... uv run pytest -m smoke
```

## Contributing

- Before opening a pull request or issue, check whether it belongs at this client level or the Coolify REST API.
- Fork this repo and submit a pull request.
- Respect Python PEPs and type inference.
- Ship unit tests with any change.
- No breaking changes unless required by the Coolify REST API.

## License

Apache License 2.0 — see [LICENSE](./LICENSE).
