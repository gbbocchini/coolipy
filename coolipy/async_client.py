"""Asynchronous coolipy client."""

from __future__ import annotations

import httpx

from coolipy._http import AsyncTransport, build_base_url, parse_response
from coolipy._response import CoolipyAPIResponse
from coolipy.exceptions import CoolipyConfigError
from coolipy.models.system import SystemMessage
from coolipy.resources.applications import AsyncApplications
from coolipy.resources.databases import AsyncDatabases
from coolipy.resources.services import AsyncServices


class AsyncCoolipy:
    """Asynchronous client for the Coolify API.

    Args:
        coolify_api_key: Bearer token used to authenticate with the Coolify API.
        coolify_endpoint: Hostname or IP of the Coolify instance.
        coolify_port: Port of the Coolify instance (ignored when ``omit_port``).
        omit_port: When ``True``, build the base URL without a port.
        http_protocol: ``"http"`` or ``"https"``.
        timeout: Request timeout in seconds.
        transport: Optional httpx async transport override (mainly for testing).
    """

    def __init__(
        self,
        coolify_api_key: str,
        coolify_endpoint: str,
        coolify_port: int = 8000,
        omit_port: bool = False,
        http_protocol: str = "http",
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if not coolify_api_key:
            raise CoolipyConfigError("coolify_api_key must be a non-empty string.")
        base_url = build_base_url(http_protocol, coolify_endpoint, coolify_port, omit_port)
        self._transport = AsyncTransport(
            base_url, coolify_api_key, timeout=timeout, transport=transport
        )
        self.applications = AsyncApplications(self._transport)
        self.databases = AsyncDatabases(self._transport)
        self.services = AsyncServices(self._transport)

    async def version(self) -> CoolipyAPIResponse[str]:
        """Get the Coolify version."""
        return parse_response(await self._transport.request("GET", "/version"), str)

    async def health(self) -> CoolipyAPIResponse[str]:
        """Run the Coolify healthcheck."""
        return parse_response(await self._transport.request("GET", "/health"), str)

    async def enable_api(self) -> CoolipyAPIResponse[SystemMessage]:
        """Enable the Coolify API (requires root permissions)."""
        return parse_response(await self._transport.request("POST", "/enable"), SystemMessage)

    async def disable_api(self) -> CoolipyAPIResponse[SystemMessage]:
        """Disable the Coolify API (requires root permissions)."""
        return parse_response(await self._transport.request("POST", "/disable"), SystemMessage)

    async def enable_mcp(self) -> CoolipyAPIResponse[SystemMessage]:
        """Enable the Coolify MCP server (requires root permissions)."""
        return parse_response(await self._transport.request("POST", "/mcp/enable"), SystemMessage)

    async def disable_mcp(self) -> CoolipyAPIResponse[SystemMessage]:
        """Disable the Coolify MCP server (requires root permissions)."""
        return parse_response(await self._transport.request("POST", "/mcp/disable"), SystemMessage)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._transport.close()

    async def __aenter__(self) -> AsyncCoolipy:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()
