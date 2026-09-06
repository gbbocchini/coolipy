"""Tags resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import MessageResponse, Tag, TagCreate, TagUpdate

TagList = list[Tag]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Tags(ResourceBase):
    """Synchronous client for Coolify tags."""

    def list(self) -> CoolipyAPIResponse[TagList]:
        """List all tags."""
        return self._get("/tags", response_model=list[Tag])

    def create(self, model: TagCreate) -> CoolipyAPIResponse[Tag]:
        """Create a tag."""
        return self._post("/tags", json=_dump(model), response_model=Tag)

    def update(self, uuid: str, model: TagUpdate) -> CoolipyAPIResponse[Tag]:
        """Update a tag by UUID."""
        return self._patch(f"/tags/{uuid}", json=_dump(model), response_model=Tag)

    def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a tag by UUID."""
        return self._delete(f"/tags/{uuid}", response_model=MessageResponse)


class AsyncTags(AsyncResourceBase):
    """Asynchronous client for Coolify tags."""

    async def list(self) -> CoolipyAPIResponse[TagList]:
        """List all tags."""
        return await self._get("/tags", response_model=list[Tag])

    async def create(self, model: TagCreate) -> CoolipyAPIResponse[Tag]:
        """Create a tag."""
        return await self._post("/tags", json=_dump(model), response_model=Tag)

    async def update(self, uuid: str, model: TagUpdate) -> CoolipyAPIResponse[Tag]:
        """Update a tag by UUID."""
        return await self._patch(f"/tags/{uuid}", json=_dump(model), response_model=Tag)

    async def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a tag by UUID."""
        return await self._delete(f"/tags/{uuid}", response_model=MessageResponse)
