import json

import httpx

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._http import AsyncTransport, SyncTransport
from coolipy.models.base import CoolipyBaseModel


class _Create(CoolipyBaseModel):
    name: str


class _Projects(ResourceBase):
    def list(self):
        return self._get("/projects", response_model=list[str])

    def create(self, model: _Create):
        return self._post("/projects", json=model.model_dump(mode="json", exclude_none=True))


def test_resource_base_get():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/projects"
        return httpx.Response(200, json=["p1", "p2"])

    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = _Projects(transport).list()
    finally:
        transport.close()

    assert result.data == ["p1", "p2"]


def test_resource_base_post_serializes_model():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/projects"
        assert json.loads(request.content) == {"name": "my-project"}
        return httpx.Response(201, json={"uuid": "abc"})

    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = _Projects(transport).create(_Create(name="my-project"))
    finally:
        transport.close()

    assert result.status_code == 201
    assert result.data == {"uuid": "abc"}


class _AsyncProjects(AsyncResourceBase):
    async def list(self):
        return await self._get("/projects", response_model=list[str])


async def test_async_resource_base_get():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/projects"
        return httpx.Response(200, json=["p1"])

    transport = AsyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = await _AsyncProjects(transport).list()
    finally:
        await transport.close()

    assert result.data == ["p1"]
