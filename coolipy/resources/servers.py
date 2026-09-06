"""Servers resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import (
    Destination,
    DestinationCreate,
    EnvironmentVariable,
    EnvironmentVariableCreate,
    MessageResponse,
    UUIDResponse,
)
from coolipy.models.servers import ServerCreateModel, ServerModel, ServerUpdateModel

ServerList = list[ServerModel]
DestinationList = list[Destination]
EnvironmentVariableList = list[EnvironmentVariable]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Servers(ResourceBase):
    """Synchronous client for Coolify servers."""

    def list(self) -> CoolipyAPIResponse[ServerList]:
        """List all servers."""
        return self._get("/servers", response_model=list[ServerModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[ServerModel]:
        """Get a server by UUID."""
        return self._get(f"/servers/{uuid}", response_model=ServerModel)

    def create(self, model: ServerCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a server."""
        return self._post("/servers", json=_dump(model), response_model=UUIDResponse)

    def update(self, uuid: str, model: ServerUpdateModel) -> CoolipyAPIResponse[ServerModel]:
        """Update a server by UUID."""
        return self._patch(f"/servers/{uuid}", json=_dump(model), response_model=ServerModel)

    def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a server by UUID."""
        return self._delete(f"/servers/{uuid}", response_model=MessageResponse)

    def resources(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List resources running on a server."""
        return self._get(f"/servers/{uuid}/resources")

    def domains(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List domains configured on a server."""
        return self._get(f"/servers/{uuid}/domains")

    def validate(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """Validate a server."""
        return self._post(f"/servers/{uuid}/validate")

    def destinations(self, server_uuid: str) -> CoolipyAPIResponse[DestinationList]:
        """List destinations for a server."""
        return self._get(f"/servers/{server_uuid}/destinations", response_model=list[Destination])

    def add_destination(
        self, server_uuid: str, model: DestinationCreate
    ) -> CoolipyAPIResponse[Any]:
        """Add a destination to a server."""
        return self._post(f"/servers/{server_uuid}/destinations", json=_dump(model))

    def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a server."""
        return self._get(f"/servers/{uuid}/envs", response_model=list[EnvironmentVariable])

    def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a server."""
        return self._post(f"/servers/{uuid}/envs", json=_dump(model), response_model=UUIDResponse)

    def delete_env(self, uuid: str, env_id: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable from a server."""
        return self._delete(f"/servers/{uuid}/envs/{env_id}", response_model=MessageResponse)


class AsyncServers(AsyncResourceBase):
    """Asynchronous client for Coolify servers."""

    async def list(self) -> CoolipyAPIResponse[ServerList]:
        """List all servers."""
        return await self._get("/servers", response_model=list[ServerModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[ServerModel]:
        """Get a server by UUID."""
        return await self._get(f"/servers/{uuid}", response_model=ServerModel)

    async def create(self, model: ServerCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a server."""
        return await self._post("/servers", json=_dump(model), response_model=UUIDResponse)

    async def update(self, uuid: str, model: ServerUpdateModel) -> CoolipyAPIResponse[ServerModel]:
        """Update a server by UUID."""
        return await self._patch(f"/servers/{uuid}", json=_dump(model), response_model=ServerModel)

    async def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a server by UUID."""
        return await self._delete(f"/servers/{uuid}", response_model=MessageResponse)

    async def resources(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List resources running on a server."""
        return await self._get(f"/servers/{uuid}/resources")

    async def domains(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List domains configured on a server."""
        return await self._get(f"/servers/{uuid}/domains")

    async def validate(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """Validate a server."""
        return await self._post(f"/servers/{uuid}/validate")

    async def destinations(self, server_uuid: str) -> CoolipyAPIResponse[DestinationList]:
        """List destinations for a server."""
        return await self._get(
            f"/servers/{server_uuid}/destinations", response_model=list[Destination]
        )

    async def add_destination(
        self, server_uuid: str, model: DestinationCreate
    ) -> CoolipyAPIResponse[Any]:
        """Add a destination to a server."""
        return await self._post(f"/servers/{server_uuid}/destinations", json=_dump(model))

    async def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a server."""
        return await self._get(f"/servers/{uuid}/envs", response_model=list[EnvironmentVariable])

    async def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a server."""
        return await self._post(
            f"/servers/{uuid}/envs", json=_dump(model), response_model=UUIDResponse
        )

    async def delete_env(self, uuid: str, env_id: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable from a server."""
        return await self._delete(f"/servers/{uuid}/envs/{env_id}", response_model=MessageResponse)
