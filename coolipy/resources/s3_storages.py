"""S3 storage resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import MessageResponse, UUIDResponse
from coolipy.models.s3_storages import (
    S3StorageCreateModel,
    S3StorageModel,
    S3StorageUpdateModel,
)

S3StorageList = list[S3StorageModel]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class S3Storages(ResourceBase):
    """Synchronous client for Coolify S3 storages."""

    def list(self) -> CoolipyAPIResponse[S3StorageList]:
        """List all S3 storages."""
        return self._get("/s3-storages", response_model=list[S3StorageModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[S3StorageModel]:
        """Get an S3 storage by UUID."""
        return self._get(f"/s3-storages/{uuid}", response_model=S3StorageModel)

    def create(self, model: S3StorageCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an S3 storage."""
        return self._post("/s3-storages", json=_dump(model), response_model=UUIDResponse)

    def update(self, uuid: str, model: S3StorageUpdateModel) -> CoolipyAPIResponse[S3StorageModel]:
        """Update an S3 storage by UUID."""
        return self._patch(f"/s3-storages/{uuid}", json=_dump(model), response_model=S3StorageModel)

    def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an S3 storage by UUID."""
        return self._delete(f"/s3-storages/{uuid}", response_model=MessageResponse)

    def validate(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """Validate an S3 storage by UUID."""
        return self._post(f"/s3-storages/{uuid}/validate")


class AsyncS3Storages(AsyncResourceBase):
    """Asynchronous client for Coolify S3 storages."""

    async def list(self) -> CoolipyAPIResponse[S3StorageList]:
        """List all S3 storages."""
        return await self._get("/s3-storages", response_model=list[S3StorageModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[S3StorageModel]:
        """Get an S3 storage by UUID."""
        return await self._get(f"/s3-storages/{uuid}", response_model=S3StorageModel)

    async def create(self, model: S3StorageCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an S3 storage."""
        return await self._post("/s3-storages", json=_dump(model), response_model=UUIDResponse)

    async def update(
        self, uuid: str, model: S3StorageUpdateModel
    ) -> CoolipyAPIResponse[S3StorageModel]:
        """Update an S3 storage by UUID."""
        return await self._patch(
            f"/s3-storages/{uuid}", json=_dump(model), response_model=S3StorageModel
        )

    async def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an S3 storage by UUID."""
        return await self._delete(f"/s3-storages/{uuid}", response_model=MessageResponse)

    async def validate(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """Validate an S3 storage by UUID."""
        return await self._post(f"/s3-storages/{uuid}/validate")
