"""Projects resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import MessageResponse, UUIDResponse
from coolipy.models.projects import (
    EnvironmentCreateModel,
    EnvironmentModel,
    EnvironmentUpdateModel,
    ProjectCreateModel,
    ProjectModel,
    ProjectUpdateModel,
)

ProjectList = list[ProjectModel]
EnvironmentList = list[EnvironmentModel]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Projects(ResourceBase):
    """Synchronous client for Coolify projects."""

    def list(self) -> CoolipyAPIResponse[ProjectList]:
        """List all projects."""
        return self._get("/projects", response_model=list[ProjectModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[ProjectModel]:
        """Get a project by UUID."""
        return self._get(f"/projects/{uuid}", response_model=ProjectModel)

    def create(self, model: ProjectCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a project."""
        return self._post("/projects", json=_dump(model), response_model=UUIDResponse)

    def update(self, uuid: str, model: ProjectUpdateModel) -> CoolipyAPIResponse[dict]:
        """Update a project by UUID."""
        return self._patch(f"/projects/{uuid}", json=_dump(model), response_model=dict)

    def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a project by UUID."""
        return self._delete(f"/projects/{uuid}", response_model=MessageResponse)

    def environment(
        self, uuid: str, environment_name_or_uuid: str
    ) -> CoolipyAPIResponse[EnvironmentModel]:
        """Get an environment by name or UUID."""
        return self._get(
            f"/projects/{uuid}/{environment_name_or_uuid}", response_model=EnvironmentModel
        )

    def environments(self, uuid: str) -> CoolipyAPIResponse[EnvironmentList]:
        """List environments for a project."""
        return self._get(f"/projects/{uuid}/environments", response_model=list[EnvironmentModel])

    def create_environment(
        self, uuid: str, model: EnvironmentCreateModel
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment for a project."""
        return self._post(
            f"/projects/{uuid}/environments", json=_dump(model), response_model=UUIDResponse
        )

    def update_environment(
        self, uuid: str, environment_name_or_uuid: str, model: EnvironmentUpdateModel
    ) -> CoolipyAPIResponse[EnvironmentModel]:
        """Update an environment by name or UUID."""
        return self._patch(
            f"/projects/{uuid}/environments/{environment_name_or_uuid}",
            json=_dump(model),
            response_model=EnvironmentModel,
        )

    def delete_environment(
        self, uuid: str, environment_name_or_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment by name or UUID."""
        return self._delete(
            f"/projects/{uuid}/environments/{environment_name_or_uuid}",
            response_model=MessageResponse,
        )


class AsyncProjects(AsyncResourceBase):
    """Asynchronous client for Coolify projects."""

    async def list(self) -> CoolipyAPIResponse[ProjectList]:
        """List all projects."""
        return await self._get("/projects", response_model=list[ProjectModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[ProjectModel]:
        """Get a project by UUID."""
        return await self._get(f"/projects/{uuid}", response_model=ProjectModel)

    async def create(self, model: ProjectCreateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a project."""
        return await self._post("/projects", json=_dump(model), response_model=UUIDResponse)

    async def update(self, uuid: str, model: ProjectUpdateModel) -> CoolipyAPIResponse[dict]:
        """Update a project by UUID."""
        return await self._patch(f"/projects/{uuid}", json=_dump(model), response_model=dict)

    async def delete(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a project by UUID."""
        return await self._delete(f"/projects/{uuid}", response_model=MessageResponse)

    async def environment(
        self, uuid: str, environment_name_or_uuid: str
    ) -> CoolipyAPIResponse[EnvironmentModel]:
        """Get an environment by name or UUID."""
        return await self._get(
            f"/projects/{uuid}/{environment_name_or_uuid}", response_model=EnvironmentModel
        )

    async def environments(self, uuid: str) -> CoolipyAPIResponse[EnvironmentList]:
        """List environments for a project."""
        return await self._get(
            f"/projects/{uuid}/environments", response_model=list[EnvironmentModel]
        )

    async def create_environment(
        self, uuid: str, model: EnvironmentCreateModel
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment for a project."""
        return await self._post(
            f"/projects/{uuid}/environments", json=_dump(model), response_model=UUIDResponse
        )

    async def update_environment(
        self, uuid: str, environment_name_or_uuid: str, model: EnvironmentUpdateModel
    ) -> CoolipyAPIResponse[EnvironmentModel]:
        """Update an environment by name or UUID."""
        return await self._patch(
            f"/projects/{uuid}/environments/{environment_name_or_uuid}",
            json=_dump(model),
            response_model=EnvironmentModel,
        )

    async def delete_environment(
        self, uuid: str, environment_name_or_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment by name or UUID."""
        return await self._delete(
            f"/projects/{uuid}/environments/{environment_name_or_uuid}",
            response_model=MessageResponse,
        )
