"""Shared base classes for coolipy resource clients."""

from __future__ import annotations

from typing import Any

from coolipy._http import AsyncTransport, SyncTransport, parse_response
from coolipy._response import CoolipyAPIResponse


class ResourceBase:
    """Base class for synchronous resource clients.

    Subclasses inject a :class:`SyncTransport` and call the ``_get``/``_post``/
    ``_patch``/``_delete`` helpers with a path and optional response model.
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = self._transport.request("GET", path, params=params)
        return parse_response(response, response_model)

    def _post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = self._transport.request("POST", path, params=params, json=json)
        return parse_response(response, response_model)

    def _patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = self._transport.request("PATCH", path, params=params, json=json)
        return parse_response(response, response_model)

    def _delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = self._transport.request("DELETE", path, params=params, json=json)
        return parse_response(response, response_model)


class AsyncResourceBase:
    """Base class for asynchronous resource clients.

    Subclasses inject an :class:`AsyncTransport` and ``await`` the ``_get``/
    ``_post``/``_patch``/``_delete`` helpers.
    """

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = await self._transport.request("GET", path, params=params)
        return parse_response(response, response_model)

    async def _post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = await self._transport.request("POST", path, params=params, json=json)
        return parse_response(response, response_model)

    async def _patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = await self._transport.request("PATCH", path, params=params, json=json)
        return parse_response(response, response_model)

    async def _delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        response_model: Any = None,
    ) -> CoolipyAPIResponse:
        response = await self._transport.request("DELETE", path, params=params, json=json)
        return parse_response(response, response_model)
