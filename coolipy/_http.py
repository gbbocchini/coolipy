"""HTTP transports for coolipy (sync + async), built on httpx."""

from __future__ import annotations

from typing import Any

import httpx
from pydantic import TypeAdapter

from coolipy._response import CoolipyAPIResponse
from coolipy.exceptions import CoolipyHTTPError

#: Every Coolify endpoint lives under this base path (see the OpenAPI ``servers`` entry).
API_PREFIX = "/api/v1"


def build_base_url(http_protocol: str, endpoint: str, port: int, omit_port: bool) -> str:
    """Build the Coolify origin URL from the connection settings."""
    host = endpoint.rstrip("/")
    if omit_port:
        return f"{http_protocol}://{host}"
    return f"{http_protocol}://{host}:{port}"


def _decode_body(response: httpx.Response) -> Any:
    """Return the JSON body, falling back to raw text for non-JSON responses."""
    try:
        return response.json()
    except ValueError:
        return response.text


def _raise_for_status(status_code: int, data: Any) -> None:
    """Raise :class:`CoolipyHTTPError` when ``status_code`` is outside the 2xx range."""
    if status_code < 400:
        return
    message = "Unknown error."
    errors = None
    if isinstance(data, dict):
        raw_message = data.get("message", "Unknown error.")
        message = raw_message if isinstance(raw_message, str) else str(raw_message)
        errors = data.get("errors")
    raise CoolipyHTTPError(status_code, message, errors=errors, response=data)


def parse_response(
    response: httpx.Response,
    response_model: Any = None,
) -> CoolipyAPIResponse:
    """Decode ``response`` and, when ``response_model`` is given, validate ``data``.

    Args:
        response: The raw httpx response.
        response_model: Optional model or generic alias (e.g. ``list[Model]``)
            used to validate the response body.

    Returns:
        A :class:`CoolipyAPIResponse` carrying the decoded/validated body.

    Raises:
        CoolipyHTTPError: When the response status code is outside the 2xx range.
    """
    data = _decode_body(response)
    _raise_for_status(response.status_code, data)
    if response_model is not None:
        data = TypeAdapter(response_model).validate_python(data)
    return CoolipyAPIResponse(
        status_code=response.status_code,
        data=data,
        headers=dict(response.headers),
    )


class SyncTransport:
    """Synchronous httpx transport bound to the Coolify API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {token}"},
            timeout=timeout,
            transport=transport,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> httpx.Response:
        """Perform a request under ``/api/v1`` and return the raw response."""
        return self._client.request(method, f"{API_PREFIX}{path}", params=params, json=json)

    def close(self) -> None:
        """Close the underlying httpx client."""
        self._client.close()

    def __enter__(self) -> SyncTransport:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncTransport:
    """Asynchronous httpx transport bound to the Coolify API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {token}"},
            timeout=timeout,
            transport=transport,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> httpx.Response:
        """Perform a request under ``/api/v1`` and return the raw response."""
        return await self._client.request(method, f"{API_PREFIX}{path}", params=params, json=json)

    async def close(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTransport:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()
