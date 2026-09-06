import httpx
import pytest

from coolipy._http import AsyncTransport, SyncTransport, build_base_url, parse_response
from coolipy.exceptions import CoolipyHTTPError
from coolipy.models.system import SystemMessage


def test_build_base_url_with_port():
    assert build_base_url("http", "localhost", 8000, False) == "http://localhost:8000"


def test_build_base_url_omit_port():
    assert (
        build_base_url("https", "coolify.example.com", 8000, True) == "https://coolify.example.com"
    )


def test_parse_response_validates_model():
    response = httpx.Response(200, json={"message": "API enabled."})
    parsed = parse_response(response, SystemMessage)
    assert parsed.status_code == 200
    assert isinstance(parsed.data, SystemMessage)
    assert parsed.data.message == "API enabled."


def test_parse_response_validates_list_alias():
    response = httpx.Response(200, json=["a", "b"])
    parsed = parse_response(response, list[str])
    assert parsed.data == ["a", "b"]


def test_parse_response_falls_back_to_text():
    response = httpx.Response(200, text="v4.0.0")
    parsed = parse_response(response, str)
    assert parsed.data == "v4.0.0"


@pytest.mark.parametrize(
    ("status", "body", "message"),
    [
        (400, {"message": "Invalid token."}, "Invalid token."),
        (401, {"message": "Unauthenticated."}, "Unauthenticated."),
        (404, {"message": "Resource not found."}, "Resource not found."),
        (429, {"message": "Rate limit exceeded."}, "Rate limit exceeded."),
    ],
)
def test_parse_response_raises_on_error(status, body, message):
    response = httpx.Response(status, json=body)
    with pytest.raises(CoolipyHTTPError) as excinfo:
        parse_response(response)
    assert excinfo.value.status_code == status
    assert excinfo.value.message == message


def test_parse_response_raises_with_validation_errors():
    response = httpx.Response(
        422, json={"message": "Validation error.", "errors": {"name": ["required"]}}
    )
    with pytest.raises(CoolipyHTTPError) as excinfo:
        parse_response(response)
    assert excinfo.value.status_code == 422
    assert excinfo.value.errors == {"name": ["required"]}


def test_sync_transport_prefix_and_auth():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/version"
        assert request.headers["Authorization"] == "Bearer abc"
        return httpx.Response(200, text="v4.0.0")

    transport = SyncTransport(
        "http://localhost:8000", "abc", transport=httpx.MockTransport(handler)
    )
    try:
        response = transport.request("GET", "/version")
        assert response.status_code == 200
    finally:
        transport.close()


async def test_async_transport_prefix_and_auth():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/version"
        assert request.headers["Authorization"] == "Bearer abc"
        return httpx.Response(200, text="v4.0.0")

    transport = AsyncTransport(
        "http://localhost:8000", "abc", transport=httpx.MockTransport(handler)
    )
    try:
        response = await transport.request("GET", "/version")
        assert response.status_code == 200
    finally:
        await transport.close()
