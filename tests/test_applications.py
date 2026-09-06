import json

import httpx

from coolipy._http import SyncTransport
from coolipy.models.applications import (
    ApplicationModel,
    ApplicationPrivateGHModelCreate,
    ApplicationPublicModelCreate,
)
from coolipy.models.common import EnvironmentVariable, EnvironmentVariableCreate
from coolipy.resources.applications import Applications


def _apps(handler):
    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    return Applications(transport), transport


def test_list_applications():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/applications"
        return httpx.Response(200, json=[{"uuid": "a", "name": "app"}])

    apps, transport = _apps(handler)
    try:
        result = apps.list()
    finally:
        transport.close()

    assert isinstance(result.data[0], ApplicationModel)
    assert result.data[0].uuid == "a"


def test_get_application():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/applications/abc"
        return httpx.Response(200, json={"uuid": "abc", "name": "app"})

    apps, transport = _apps(handler)
    try:
        result = apps.get("abc")
    finally:
        transport.close()

    assert result.data.name == "app"


def test_create_public_application_serializes_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/applications/public"
        assert json.loads(request.content) == {"name": "app", "build_pack": "nixpacks"}
        return httpx.Response(201, json={"uuid": "xyz"})

    apps, transport = _apps(handler)
    try:
        result = apps.create(ApplicationPublicModelCreate(name="app", build_pack="nixpacks"))
    finally:
        transport.close()

    assert result.data.uuid == "xyz"


def test_create_private_github_application_uses_correct_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/applications/private-github-app"
        return httpx.Response(201, json={"uuid": "xyz"})

    apps, transport = _apps(handler)
    try:
        apps.create(ApplicationPrivateGHModelCreate(name="app"))
    finally:
        transport.close()


def test_list_envs():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/applications/abc/envs"
        return httpx.Response(200, json=[{"key": "FOO", "value": "bar"}])

    apps, transport = _apps(handler)
    try:
        result = apps.envs("abc")
    finally:
        transport.close()

    assert isinstance(result.data[0], EnvironmentVariable)
    assert result.data[0].key == "FOO"


def test_create_env_serializes_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/applications/abc/envs"
        assert json.loads(request.content) == {"key": "FOO", "value": "bar"}
        return httpx.Response(201, json={"uuid": "env-uuid"})

    apps, transport = _apps(handler)
    try:
        result = apps.create_env("abc", EnvironmentVariableCreate(key="FOO", value="bar"))
    finally:
        transport.close()

    assert result.data.uuid == "env-uuid"
