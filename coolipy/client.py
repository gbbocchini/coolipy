"""Synchronous coolipy client."""

from __future__ import annotations

import httpx

from coolipy._http import SyncTransport, build_base_url, parse_response
from coolipy._response import CoolipyAPIResponse
from coolipy.exceptions import CoolipyConfigError
from coolipy.models.system import SystemMessage
from coolipy.resources.applications import Applications
from coolipy.resources.databases import Databases
from coolipy.resources.deployments import Deployments
from coolipy.resources.projects import Projects
from coolipy.resources.s3_storages import S3Storages
from coolipy.resources.security import Security
from coolipy.resources.servers import Servers
from coolipy.resources.services import Services
from coolipy.resources.tags import Tags
from coolipy.resources.teams import Teams


class Coolipy:
    """Synchronous client for the Coolify API.

    Args:
        coolify_api_key: Bearer token used to authenticate with the Coolify API.
        coolify_endpoint: Hostname or IP of the Coolify instance.
        coolify_port: Port of the Coolify instance (ignored when ``omit_port``).
        omit_port: When ``True``, build the base URL without a port.
        http_protocol: ``"http"`` or ``"https"``.
        timeout: Request timeout in seconds.
        transport: Optional httpx transport override (mainly for testing).
    """

    def __init__(
        self,
        coolify_api_key: str,
        coolify_endpoint: str,
        coolify_port: int = 8000,
        omit_port: bool = False,
        http_protocol: str = "http",
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not coolify_api_key:
            raise CoolipyConfigError("coolify_api_key must be a non-empty string.")
        base_url = build_base_url(http_protocol, coolify_endpoint, coolify_port, omit_port)
        self._transport = SyncTransport(
            base_url, coolify_api_key, timeout=timeout, transport=transport
        )
        self.applications = Applications(self._transport)
        self.databases = Databases(self._transport)
        self.services = Services(self._transport)
        self.servers = Servers(self._transport)
        self.projects = Projects(self._transport)
        self.teams = Teams(self._transport)
        self.deployments = Deployments(self._transport)
        self.tags = Tags(self._transport)
        self.s3_storages = S3Storages(self._transport)
        self.security = Security(self._transport)

    def version(self) -> CoolipyAPIResponse[str]:
        """Get the Coolify version."""
        return parse_response(self._transport.request("GET", "/version"), str)

    def health(self) -> CoolipyAPIResponse[str]:
        """Run the Coolify healthcheck."""
        return parse_response(self._transport.request("GET", "/health"), str)

    def enable_api(self) -> CoolipyAPIResponse[SystemMessage]:
        """Enable the Coolify API (requires root permissions)."""
        return parse_response(self._transport.request("POST", "/enable"), SystemMessage)

    def disable_api(self) -> CoolipyAPIResponse[SystemMessage]:
        """Disable the Coolify API (requires root permissions)."""
        return parse_response(self._transport.request("POST", "/disable"), SystemMessage)

    def enable_mcp(self) -> CoolipyAPIResponse[SystemMessage]:
        """Enable the Coolify MCP server (requires root permissions)."""
        return parse_response(self._transport.request("POST", "/mcp/enable"), SystemMessage)

    def disable_mcp(self) -> CoolipyAPIResponse[SystemMessage]:
        """Disable the Coolify MCP server (requires root permissions)."""
        return parse_response(self._transport.request("POST", "/mcp/disable"), SystemMessage)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._transport.close()

    def __enter__(self) -> Coolipy:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
