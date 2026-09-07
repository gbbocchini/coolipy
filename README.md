<h1 align="center">coolipy</h1>

<p align="center">
  <strong>The (un)official Python client for <a href="https://coolify.io">Coolify</a></strong><br />
  Synchronous <em>and</em> asynchronous · typed <a href="https://docs.pydantic.dev/">pydantic</a> models · no raw dicts, no manual JSON
</p>

<p align="center">
  <a href="https://pypi.org/project/coolipy/"><img src="https://img.shields.io/pypi/v/coolipy" alt="PyPI" /></a>
  <a href="https://pypi.org/project/coolipy/"><img src="https://img.shields.io/pypi/pyversions/coolipy" alt="Python versions" /></a>
  <a href="https://pypi.org/project/coolipy/"><img src="https://img.shields.io/pypi/dm/coolipy" alt="Downloads" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License" /></a>
  <a href="https://github.com/gbbocchini/coolipy/actions/workflows/ci.yml"><img src="https://github.com/gbbocchini/coolipy/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
</p>

---

- 📚 **Lib docs:** https://coolipydocs.gabrielbocchini.com.br/
- 🧭 **Coolify API docs:** https://coolify.io/docs/api

## 🚀 Installation

```bash
pip install coolipy
# or
uv add coolipy
```

Requires **Python 3.10+**. Runtime dependencies: [`httpx`](https://github.com/encode/httpx) and [`pydantic`](https://docs.pydantic.dev/).

## ✨ Features

| | |
| --- | --- |
| ⚡ **Sync + async** | One package, two clients — `Coolipy` and `AsyncCoolipy` |
| 🧱 **Typed models** | Every request and response is a `pydantic` model |
| 📦 **One envelope** | `CoolipyAPIResponse[T]` → `status_code`, validated `data`, `headers` |
| 🚨 **Typed errors** | `CoolipyHTTPError` carries the API's validation details |
| 🔌 **httpx + DI** | Dependency-injected transport — trivial to mock in tests |

## ⚡ Quick start

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
print(resp.data)         # '4.3.17'

client.close()
```

Use it as a context manager to close automatically:

```python
with Coolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    print(client.health().data)  # 'OK'
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

## 🧰 Resources

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

## 📦 Responses

Every method returns a [`CoolipyAPIResponse`](coolipy/_response.py) with three fields:

| Field | Type | Description |
| --- | --- | --- |
| `status_code` | `int` | HTTP status code. |
| `data` | `T` | Parsed body, validated against a model. |
| `headers` | `dict[str, str]` | Response headers. |

```python
resp = client.enable_api()
print(resp.data)          # SystemMessage(message='API enabled.')
print(resp.data.message)  # 'API enabled.'
```

## 🧱 Models

Every request and response body is a `pydantic` model deriving from [`CoolipyBaseModel`](coolipy/models/base.py). Response models are tolerant: every field is optional and unknown fields are ignored, so they never fail against a live instance.

- **Request models** — `*Create` / `*Update` classes you build and pass in (e.g. `ProjectCreateModel`, `ApplicationDockerImageModelCreate`, `PostgreSQLModelCreate`). Unset fields are omitted from the request body.
- **Response models** — `*Model` classes returned in `resp.data` (e.g. `ProjectModel`, `ServerModel`, `ApplicationModel`).

Enums mirror the API's string-constrained fields:

```python
from coolipy.enums import BuildPack, ProxyType, ServiceType

BuildPack.NIXPACKS.value   # 'nixpacks'
BuildPack.RAILPACK.value   # 'railpack'
ProxyType.NONE.value       # 'none'
```

## 💡 Usage examples

All examples below were captured against a live Coolify instance (`v4.3.17`).

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
#   ProjectModel(id=7, uuid='mawhjk3svlsd9v9dujlck4cq',
#                name='coolipy-smoke-apps-async', description=''),
# ]
```

### Servers

```python
resp = client.servers.list()
server = resp.data[0]
print(server)
# ServerModel(
#     uuid='g7jdko9weqgokkm7m9lhkzqb',
#     name='localhost',
#     ip='host.docker.internal',
#     user='root',
#     port=22,
#     is_coolify_host=True,
#     is_reachable=True,
#     is_usable=True,
#     proxy={'redirect_enabled': True},
#     settings=ServerSetting(id=1, concurrent_builds=2, ...),
# )
```

### Applications — from a ready-to-go Docker image

```python
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
resp = client.applications.create(app)
print(resp.data)  # UUIDResponse(uuid='6zacuhbss0pnxtjihzmxolds')

resp = client.applications.list()
app = resp.data[0]
print(app.docker_registry_image_name, app.build_pack, app.fqdn)
# nginx dockerimage http://6zacuhbss0pnxtjihzmxolds.178.104.56.250.sslip.io
```

Applications can also be created from a public/private git repository, a deploy key, or a Dockerfile — `ApplicationPublicModelCreate`, `ApplicationPrivateGHModelCreate`, `ApplicationPrivateDeployKeyModelCreate`, `ApplicationDockerfileModelCreate`.

### Databases

```python
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
resp = client.databases.create(db)
print(resp.data)  # UUIDResponse(uuid='...')
```

Eight database types are supported: `PostgreSQLModelCreate`, `MySQLModelCreate`, `MariaDBModelCreate`, `MongoDBModelCreate`, `RedisModelCreate`, `ClickhouseModelCreate`, `DragonflyModelCreate`, `KeyDBModelCreate`.

### Services

```python
from coolipy.models.services import ServiceCreateModel

service = ServiceCreateModel(
    name="my-service",
    project_uuid="your_project_uuid",
    server_uuid="your_server_uuid",
    environment_name="production",
    docker_compose_raw="<base64 docker-compose.yml>",
)
resp = client.services.create(service)
```

### Teams & members

```python
resp = client.teams.current()
print(resp.data)
# TeamModel(id=0, name='Root Team', personal_team=True, ...)

resp = client.teams.current_members()
print(resp.data)
# [UserModel(id=0, name='Gabriel B. Bocchini', email='gabrielbocchini@gmail.com', ...)]
```

### Tags, private keys, S3 storages

```python
resp = client.tags.list()
print(resp.data)  # [Tag(uuid='cz8op2sw7b0ysjvjq9ykeips', name='coolipy-smoke-tag', ...)]

resp = client.security.list()
print(resp.data)  # [PrivateKeyModel(uuid='...', name="localhost's key", is_git_related=False, ...)]

resp = client.s3_storages.list()
print(resp.data)  # []
```

### Deployments

```python
resp = client.deployments.deploy(tag="my-tag", force=True)
print(resp.data)
# DeployResponse(deployments=[DeploymentEntry(message='...', resource_uuid='...', deployment_uuid='...')])
```

### Async

Every method has an async equivalent on `AsyncCoolipy`:

```python
async with AsyncCoolipy("YOUR_API_TOKEN", "your-coolify-instance.com") as client:
    resp = await client.projects.list()
    print(resp.data)
```

## 🚨 Errors

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

## ⚙️ Configuration

Both clients take the same arguments:

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `coolify_api_key` | `str` | — | Bearer token for the Coolify API. |
| `coolify_endpoint` | `str` | — | Hostname/IP of the Coolify instance. |
| `coolify_port` | `int` | `8000` | Port (ignored when `omit_port=True`). |
| `omit_port` | `bool` | `False` | Build the base URL without a port. |
| `http_protocol` | `str` | `"http"` | `"http"` or `"https"`. |
| `timeout` | `float` | `30.0` | Request timeout in seconds. |

## 📈 Status

Coolipy **1.0.0** covers the full token-gated Coolify API surface — applications, databases, services, servers, projects, environments, teams, deployments, tags, S3 storages, private keys, shared envs, and the system endpoints — in both sync and async flavours. The suite is verified against a live Coolify instance via the smoke tests in [`tests/smoke/`](tests/smoke/).

## 🛠️ Development

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

Regenerate the API documentation (rendered with [pdoc3](https://pdoc3.github.io/pdoc/)):

```bash
uv run python docs/build_docs.py
```

This runs `pdoc` with the `docs/templates` overrides (SEO/social/LLM metadata) and
writes `sitemap.xml`, `robots.txt`, `llms.txt` and `llms-full.txt` into `html/coolipy/`.

## 🤝 Contributing

- Before opening a pull request or issue, check whether it belongs at this client level or the Coolify REST API.
- Fork this repo and submit a pull request.
- Respect Python PEPs and type inference.
- Ship unit tests with any change.
- No breaking changes unless required by the Coolify REST API.

## 📄 License

Apache License 2.0 — see [LICENSE](./LICENSE).
