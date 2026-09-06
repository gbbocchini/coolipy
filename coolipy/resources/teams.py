"""Teams resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.common import (
    EnvironmentVariable,
    EnvironmentVariableCreate,
    EnvironmentVariableUpdate,
    MessageResponse,
    UUIDResponse,
)
from coolipy.models.teams import TeamModel, UserModel

TeamList = list[TeamModel]
UserList = list[UserModel]
EnvironmentVariableList = list[EnvironmentVariable]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Teams(ResourceBase):
    """Synchronous client for Coolify teams and shared envs."""

    def list(self) -> CoolipyAPIResponse[TeamList]:
        """List all teams."""
        return self._get("/teams", response_model=list[TeamModel])

    def get(self, team_id: int) -> CoolipyAPIResponse[TeamModel]:
        """Get a team by ID."""
        return self._get(f"/teams/{team_id}", response_model=TeamModel)

    def members(self, team_id: int) -> CoolipyAPIResponse[UserList]:
        """List members of a team."""
        return self._get(f"/teams/{team_id}/members", response_model=list[UserModel])

    def current(self) -> CoolipyAPIResponse[TeamModel]:
        """Get the authenticated team."""
        return self._get("/team", response_model=TeamModel)

    def current_members(self) -> CoolipyAPIResponse[UserList]:
        """List members of the authenticated team."""
        return self._get("/team/members", response_model=list[UserModel])

    def envs(self) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List shared environment variables."""
        return self._get("/team/envs", response_model=list[EnvironmentVariable])

    def create_env(self, model: EnvironmentVariableCreate) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a shared environment variable."""
        return self._post("/team/envs", json=_dump(model), response_model=UUIDResponse)

    def update_env(
        self, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update a shared environment variable."""
        return self._patch("/team/envs", json=_dump(model), response_model=EnvironmentVariable)

    def delete_env(self, env_id: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a shared environment variable."""
        return self._delete(f"/team/envs/{env_id}", response_model=MessageResponse)


class AsyncTeams(AsyncResourceBase):
    """Asynchronous client for Coolify teams and shared envs."""

    async def list(self) -> CoolipyAPIResponse[TeamList]:
        """List all teams."""
        return await self._get("/teams", response_model=list[TeamModel])

    async def get(self, team_id: int) -> CoolipyAPIResponse[TeamModel]:
        """Get a team by ID."""
        return await self._get(f"/teams/{team_id}", response_model=TeamModel)

    async def members(self, team_id: int) -> CoolipyAPIResponse[UserList]:
        """List members of a team."""
        return await self._get(f"/teams/{team_id}/members", response_model=list[UserModel])

    async def current(self) -> CoolipyAPIResponse[TeamModel]:
        """Get the authenticated team."""
        return await self._get("/team", response_model=TeamModel)

    async def current_members(self) -> CoolipyAPIResponse[UserList]:
        """List members of the authenticated team."""
        return await self._get("/team/members", response_model=list[UserModel])

    async def envs(self) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List shared environment variables."""
        return await self._get("/team/envs", response_model=list[EnvironmentVariable])

    async def create_env(
        self, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create a shared environment variable."""
        return await self._post("/team/envs", json=_dump(model), response_model=UUIDResponse)

    async def update_env(
        self, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update a shared environment variable."""
        return await self._patch(
            "/team/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    async def delete_env(self, env_id: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a shared environment variable."""
        return await self._delete(f"/team/envs/{env_id}", response_model=MessageResponse)
