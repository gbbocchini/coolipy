import httpx
import pytest

from coolipy import AsyncCoolipy, Coolipy
from coolipy.exceptions import CoolipyConfigError


def test_coolipy_version():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/version"
        return httpx.Response(200, text="v4.0.0")

    with Coolipy("key", "localhost", transport=httpx.MockTransport(handler)) as client:
        result = client.version()

    assert result.status_code == 200
    assert result.data == "v4.0.0"


def test_coolipy_enable_api():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/enable"
        return httpx.Response(200, json={"message": "API enabled."})

    client = Coolipy("key", "localhost", transport=httpx.MockTransport(handler))
    try:
        result = client.enable_api()
    finally:
        client.close()

    assert result.data.message == "API enabled."


def test_coolipy_requires_api_key():
    with pytest.raises(CoolipyConfigError):
        Coolipy("", "localhost")


async def test_async_coolipy_version():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/version"
        return httpx.Response(200, text="v4.0.0")

    async with AsyncCoolipy("key", "localhost", transport=httpx.MockTransport(handler)) as client:
        result = await client.version()

    assert result.data == "v4.0.0"


async def test_async_coolipy_health():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/health"
        return httpx.Response(200, text="OK")

    client = AsyncCoolipy("key", "localhost", transport=httpx.MockTransport(handler))
    try:
        result = await client.health()
    finally:
        await client.close()

    assert result.data == "OK"
