"""Deployments resource clients (sync + async)."""

from __future__ import annotations

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.models.applications import ApplicationModel
from coolipy.models.deployments import DeploymentModel, DeployResponse

DeploymentList = list[DeploymentModel]
ApplicationList = list[ApplicationModel]


class Deployments(ResourceBase):
    """Synchronous client for Coolify deployments."""

    def list(self) -> CoolipyAPIResponse[DeploymentList]:
        """List currently running deployments."""
        return self._get("/deployments", response_model=list[DeploymentModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[DeploymentModel]:
        """Get a deployment by UUID."""
        return self._get(f"/deployments/{uuid}", response_model=DeploymentModel)

    def cancel(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """Cancel a deployment by UUID."""
        return self._post(f"/deployments/{uuid}/cancel", response_model=dict)

    def deploy(
        self,
        *,
        tag: str | None = None,
        uuid: str | None = None,
        force: bool | None = None,
        pr: int | None = None,
        pull_request_id: int | None = None,
        docker_tag: str | None = None,
    ) -> CoolipyAPIResponse[DeployResponse]:
        """Deploy resources by tag or UUID."""
        params: dict[str, object] = {}
        if tag is not None:
            params["tag"] = tag
        if uuid is not None:
            params["uuid"] = uuid
        if force is not None:
            params["force"] = force
        if pr is not None:
            params["pr"] = pr
        if pull_request_id is not None:
            params["pull_request_id"] = pull_request_id
        if docker_tag is not None:
            params["docker_tag"] = docker_tag
        return self._post("/deploy", params=params, response_model=DeployResponse)

    def application_deployments(
        self, uuid: str, *, skip: int = 0, take: int = 10
    ) -> CoolipyAPIResponse[ApplicationList]:
        """List deployments for an application."""
        return self._get(
            f"/deployments/applications/{uuid}",
            params={"skip": skip, "take": take},
            response_model=list[ApplicationModel],
        )


class AsyncDeployments(AsyncResourceBase):
    """Asynchronous client for Coolify deployments."""

    async def list(self) -> CoolipyAPIResponse[DeploymentList]:
        """List currently running deployments."""
        return await self._get("/deployments", response_model=list[DeploymentModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[DeploymentModel]:
        """Get a deployment by UUID."""
        return await self._get(f"/deployments/{uuid}", response_model=DeploymentModel)

    async def cancel(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """Cancel a deployment by UUID."""
        return await self._post(f"/deployments/{uuid}/cancel", response_model=dict)

    async def deploy(
        self,
        *,
        tag: str | None = None,
        uuid: str | None = None,
        force: bool | None = None,
        pr: int | None = None,
        pull_request_id: int | None = None,
        docker_tag: str | None = None,
    ) -> CoolipyAPIResponse[DeployResponse]:
        """Deploy resources by tag or UUID."""
        params: dict[str, object] = {}
        if tag is not None:
            params["tag"] = tag
        if uuid is not None:
            params["uuid"] = uuid
        if force is not None:
            params["force"] = force
        if pr is not None:
            params["pr"] = pr
        if pull_request_id is not None:
            params["pull_request_id"] = pull_request_id
        if docker_tag is not None:
            params["docker_tag"] = docker_tag
        return await self._post("/deploy", params=params, response_model=DeployResponse)

    async def application_deployments(
        self, uuid: str, *, skip: int = 0, take: int = 10
    ) -> CoolipyAPIResponse[ApplicationList]:
        """List deployments for an application."""
        return await self._get(
            f"/deployments/applications/{uuid}",
            params={"skip": skip, "take": take},
            response_model=list[ApplicationModel],
        )
