"""Security (private keys) resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import MessageResponse, UUIDResponse
from coolipy.models.security import (
    PrivateKeyCreateModel,
    PrivateKeyModel,
    PrivateKeyUpdateModel,
)

PrivateKeyList = list[PrivateKeyModel]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Security(ResourceBase):
    """Synchronous client for Coolify private keys."""

    def list(self) -> CoolipyAPIResponse[PrivateKeyList]:
        """List all private keys."""
        return self._get("/security/keys", response_model=list[PrivateKeyModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[PrivateKeyModel]:
        """Get a private key by UUID."""
        return self._get(f"/security/keys/{uuid}", response_model=PrivateKeyModel)

    def create(self, model: PrivateKeyCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a private key."""
        return self._post("/security/keys", json=_dump(model), response_model=UUIDResponse)

    def update(self, uuid: str, model: PrivateKeyUpdateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Update a private key by UUID."""
        return self._patch(f"/security/keys/{uuid}", json=_dump(model), response_model=UUIDResponse)

    def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a private key by UUID."""
        return self._delete(f"/security/keys/{uuid}", response_model=MessageResponse)


class AsyncSecurity(AsyncResourceBase):
    """Asynchronous client for Coolify private keys."""

    async def list(self) -> CoolipyAPIResponse[PrivateKeyList]:
        """List all private keys."""
        return await self._get("/security/keys", response_model=list[PrivateKeyModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[PrivateKeyModel]:
        """Get a private key by UUID."""
        return await self._get(f"/security/keys/{uuid}", response_model=PrivateKeyModel)

    async def create(self, model: PrivateKeyCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a private key."""
        return await self._post("/security/keys", json=_dump(model), response_model=UUIDResponse)

    async def update(
        self, uuid: str, model: PrivateKeyUpdateModel
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Update a private key by UUID."""
        return await self._patch(
            f"/security/keys/{uuid}", json=_dump(model), response_model=UUIDResponse
        )

    async def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a private key by UUID."""
        return await self._delete(f"/security/keys/{uuid}", response_model=MessageResponse)
