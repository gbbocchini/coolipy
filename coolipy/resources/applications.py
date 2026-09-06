"""Applications resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.exceptions import CoolipyValidationError
from coolipy.models.applications import (
    ApplicationDockerfileModelCreate,
    ApplicationDockerImageModelCreate,
    ApplicationModel,
    ApplicationPrivateDeployKeyModelCreate,
    ApplicationPrivateGHModelCreate,
    ApplicationPublicModelCreate,
    ApplicationUpdateModel,
)
from coolipy.models.common import (
    BulkEnvsUpdate,
    DeploymentQueuedResponse,
    EnvironmentVariable,
    EnvironmentVariableCreate,
    EnvironmentVariableUpdate,
    Logs,
    MessageResponse,
    ScheduledTask,
    ScheduledTaskCreate,
    ScheduledTaskExecution,
    ScheduledTaskUpdate,
    StorageCreate,
    StorageUpdate,
    Tag,
    TagsCreate,
    UUIDResponse,
    VolumeBackupScheduleRequest,
    VolumeBackupScheduleResponse,
)

ApplicationList = list[ApplicationModel]
EnvironmentVariableList = list[EnvironmentVariable]
TagList = list[Tag]
ScheduledTaskList = list[ScheduledTask]
ScheduledTaskExecutionList = list[ScheduledTaskExecution]


_APPLICATION_CREATE_PATHS: dict[type, str] = {
    ApplicationPublicModelCreate: "/applications/public",
    ApplicationPrivateGHModelCreate: "/applications/private-github-app",
    ApplicationPrivateDeployKeyModelCreate: "/applications/private-deploy-key",
    ApplicationDockerfileModelCreate: "/applications/dockerfile",
    ApplicationDockerImageModelCreate: "/applications/dockerimage",
}


def _dump(model: Any) -> dict[str, Any]:
    """Serialize a request model, omitting unset fields."""
    return model.model_dump(mode="json", exclude_none=True)


class Applications(ResourceBase):
    """Synchronous client for Coolify applications."""

    def list(self) -> CoolipyAPIResponse[ApplicationList]:
        """List all applications."""
        return self._get("/applications", response_model=list[ApplicationModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[ApplicationModel]:
        """Get an application by UUID."""
        return self._get(f"/applications/{uuid}", response_model=ApplicationModel)

    def create(
        self,
        model: ApplicationPublicModelCreate
        | ApplicationPrivateGHModelCreate
        | ApplicationPrivateDeployKeyModelCreate
        | ApplicationDockerfileModelCreate
        | ApplicationDockerImageModelCreate,
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an application from one of the supported create models."""
        path = _APPLICATION_CREATE_PATHS.get(type(model))
        if path is None:
            raise CoolipyValidationError(
                f"Unsupported application create model: {type(model).__name__}"
            )
        return self._post(path, json=_dump(model), response_model=UUIDResponse)

    def update(self, uuid: str, model: ApplicationUpdateModel) -> CoolipyAPIResponse[UUIDResponse]:
        """Update an application by UUID."""
        return self._patch(f"/applications/{uuid}", json=_dump(model), response_model=UUIDResponse)

    def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an application by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return self._delete(f"/applications/{uuid}", params=params, response_model=MessageResponse)

    def logs(
        self, uuid: str, *, lines: int = 100, show_timestamps: bool = False
    ) -> CoolipyAPIResponse[Logs]:
        """Get application logs."""
        params = {"lines": lines, "show_timestamps": show_timestamps}
        return self._get(f"/applications/{uuid}/logs", params=params, response_model=Logs)

    def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for an application."""
        return self._get(f"/applications/{uuid}/envs", response_model=list[EnvironmentVariable])

    def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for an application."""
        return self._post(
            f"/applications/{uuid}/envs", json=_dump(model), response_model=UUIDResponse
        )

    def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for an application."""
        return self._patch(
            f"/applications/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for an application."""
        return self._patch(
            f"/applications/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return self._delete(f"/applications/{uuid}/envs/{env_uuid}", response_model=MessageResponse)

    def start(
        self, uuid: str, *, force: bool = False, instant_deploy: bool = False
    ) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start an application."""
        params = {"force": force, "instant_deploy": instant_deploy}
        return self._post(
            f"/applications/{uuid}/start", params=params, response_model=DeploymentQueuedResponse
        )

    def stop(
        self, uuid: str, *, docker_cleanup: bool = True
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Stop an application."""
        return self._post(
            f"/applications/{uuid}/stop",
            params={"docker_cleanup": docker_cleanup},
            response_model=MessageResponse,
        )

    def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart an application."""
        return self._post(f"/applications/{uuid}/restart", response_model=DeploymentQueuedResponse)

    def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move an application to another environment."""
        return self._post(
            f"/applications/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate an application to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return self._post(f"/applications/{uuid}/migrate", json=body)

    def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for an application."""
        return self._get(f"/applications/{uuid}/storages", response_model=dict)

    def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for an application."""
        return self._post(f"/applications/{uuid}/storages", json=_dump(model), response_model=dict)

    def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for an application."""
        return self._patch(f"/applications/{uuid}/storages", json=_dump(model), response_model=dict)

    def delete_storage(self, uuid: str, storage_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return self._delete(
            f"/applications/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    def delete_preview(
        self, uuid: str, pull_request_id: int
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a preview deployment by pull request ID."""
        return self._delete(
            f"/applications/{uuid}/previews/{pull_request_id}", response_model=MessageResponse
        )

    def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for an application."""
        return self._get(f"/applications/{uuid}/tags", response_model=list[Tag])

    def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to an application."""
        return self._post(f"/applications/{uuid}/tags", json=_dump(model), response_model=list[Tag])

    def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from an application."""
        return self._delete(f"/applications/{uuid}/tags/{tag_uuid}")

    def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone an application into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return self._post(f"/applications/{uuid}/clone", json=body, response_model=dict)

    def rollback_images(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List available rollback images for an application."""
        return self._get(f"/applications/{uuid}/rollback-images", response_model=dict)

    def rollback(self, uuid: str, commit: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Queue a rollback deployment for an application."""
        return self._post(
            f"/applications/{uuid}/rollback",
            json={"commit": commit},
            response_model=DeploymentQueuedResponse,
        )

    def destinations(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List destinations for an application."""
        return self._get(f"/applications/{uuid}/destinations")

    def add_destination(self, uuid: str, destination_uuid: str) -> CoolipyAPIResponse[Any]:
        """Attach an additional destination to an application."""
        return self._post(
            f"/applications/{uuid}/destinations", json={"destination_uuid": destination_uuid}
        )

    def delete_destination(self, uuid: str, destination_uuid: str) -> CoolipyAPIResponse[Any]:
        """Detach an additional destination from an application."""
        return self._delete(f"/applications/{uuid}/destinations/{destination_uuid}")

    def scheduled_tasks(self, uuid: str) -> CoolipyAPIResponse[ScheduledTaskList]:
        """List scheduled tasks for an application."""
        return self._get(
            f"/applications/{uuid}/scheduled-tasks", response_model=list[ScheduledTask]
        )

    def create_scheduled_task(
        self, uuid: str, model: ScheduledTaskCreate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Create a scheduled task for an application."""
        return self._post(
            f"/applications/{uuid}/scheduled-tasks", json=_dump(model), response_model=ScheduledTask
        )

    def update_scheduled_task(
        self, uuid: str, task_uuid: str, model: ScheduledTaskUpdate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Update a scheduled task by UUID."""
        return self._patch(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}",
            json=_dump(model),
            response_model=ScheduledTask,
        )

    def delete_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a scheduled task by UUID."""
        return self._delete(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}", response_model=MessageResponse
        )

    def scheduled_task_executions(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[ScheduledTaskExecutionList]:
        """List executions of a scheduled task."""
        return self._get(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}/executions",
            response_model=list[ScheduledTaskExecution],
        )

    def execute_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Execute a scheduled task now."""
        return self._post(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}/execute",
            response_model=MessageResponse,
        )

    def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return self._put(
            f"/applications/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return self._delete(
            f"/applications/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return self._post(
            f"/applications/{uuid}/storages/{storage_uuid}/backups/run",
            response_model=MessageResponse,
        )


class AsyncApplications(AsyncResourceBase):
    """Asynchronous client for Coolify applications."""

    async def list(self) -> CoolipyAPIResponse[ApplicationList]:
        """List all applications."""
        return await self._get("/applications", response_model=list[ApplicationModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[ApplicationModel]:
        """Get an application by UUID."""
        return await self._get(f"/applications/{uuid}", response_model=ApplicationModel)

    async def create(self, model: Any) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an application from one of the supported create models."""
        path = _APPLICATION_CREATE_PATHS.get(type(model))
        if path is None:
            raise CoolipyValidationError(
                f"Unsupported application create model: {type(model).__name__}"
            )
        return await self._post(path, json=_dump(model), response_model=UUIDResponse)

    async def update(
        self, uuid: str, model: ApplicationUpdateModel
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Update an application by UUID."""
        return await self._patch(
            f"/applications/{uuid}", json=_dump(model), response_model=UUIDResponse
        )

    async def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an application by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return await self._delete(
            f"/applications/{uuid}", params=params, response_model=MessageResponse
        )

    async def logs(
        self, uuid: str, *, lines: int = 100, show_timestamps: bool = False
    ) -> CoolipyAPIResponse[Logs]:
        """Get application logs."""
        params = {"lines": lines, "show_timestamps": show_timestamps}
        return await self._get(f"/applications/{uuid}/logs", params=params, response_model=Logs)

    async def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for an application."""
        return await self._get(
            f"/applications/{uuid}/envs", response_model=list[EnvironmentVariable]
        )

    async def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for an application."""
        return await self._post(
            f"/applications/{uuid}/envs", json=_dump(model), response_model=UUIDResponse
        )

    async def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for an application."""
        return await self._patch(
            f"/applications/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    async def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for an application."""
        return await self._patch(
            f"/applications/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    async def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return await self._delete(
            f"/applications/{uuid}/envs/{env_uuid}", response_model=MessageResponse
        )

    async def start(
        self, uuid: str, *, force: bool = False, instant_deploy: bool = False
    ) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start an application."""
        params = {"force": force, "instant_deploy": instant_deploy}
        return await self._post(
            f"/applications/{uuid}/start", params=params, response_model=DeploymentQueuedResponse
        )

    async def stop(
        self, uuid: str, *, docker_cleanup: bool = True
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Stop an application."""
        return await self._post(
            f"/applications/{uuid}/stop",
            params={"docker_cleanup": docker_cleanup},
            response_model=MessageResponse,
        )

    async def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart an application."""
        return await self._post(
            f"/applications/{uuid}/restart", response_model=DeploymentQueuedResponse
        )

    async def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move an application to another environment."""
        return await self._post(
            f"/applications/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    async def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate an application to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return await self._post(f"/applications/{uuid}/migrate", json=body)

    async def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for an application."""
        return await self._get(f"/applications/{uuid}/storages", response_model=dict)

    async def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for an application."""
        return await self._post(
            f"/applications/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for an application."""
        return await self._patch(
            f"/applications/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def delete_storage(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return await self._delete(
            f"/applications/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    async def delete_preview(
        self, uuid: str, pull_request_id: int
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a preview deployment by pull request ID."""
        return await self._delete(
            f"/applications/{uuid}/previews/{pull_request_id}", response_model=MessageResponse
        )

    async def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for an application."""
        return await self._get(f"/applications/{uuid}/tags", response_model=list[Tag])

    async def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to an application."""
        return await self._post(
            f"/applications/{uuid}/tags", json=_dump(model), response_model=list[Tag]
        )

    async def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from an application."""
        return await self._delete(f"/applications/{uuid}/tags/{tag_uuid}")

    async def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone an application into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return await self._post(f"/applications/{uuid}/clone", json=body, response_model=dict)

    async def rollback_images(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List available rollback images for an application."""
        return await self._get(f"/applications/{uuid}/rollback-images", response_model=dict)

    async def rollback(
        self, uuid: str, commit: str
    ) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Queue a rollback deployment for an application."""
        return await self._post(
            f"/applications/{uuid}/rollback",
            json={"commit": commit},
            response_model=DeploymentQueuedResponse,
        )

    async def destinations(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List destinations for an application."""
        return await self._get(f"/applications/{uuid}/destinations")

    async def add_destination(self, uuid: str, destination_uuid: str) -> CoolipyAPIResponse[Any]:
        """Attach an additional destination to an application."""
        return await self._post(
            f"/applications/{uuid}/destinations", json={"destination_uuid": destination_uuid}
        )

    async def delete_destination(self, uuid: str, destination_uuid: str) -> CoolipyAPIResponse[Any]:
        """Detach an additional destination from an application."""
        return await self._delete(f"/applications/{uuid}/destinations/{destination_uuid}")

    async def scheduled_tasks(self, uuid: str) -> CoolipyAPIResponse[ScheduledTaskList]:
        """List scheduled tasks for an application."""
        return await self._get(
            f"/applications/{uuid}/scheduled-tasks", response_model=list[ScheduledTask]
        )

    async def create_scheduled_task(
        self, uuid: str, model: ScheduledTaskCreate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Create a scheduled task for an application."""
        return await self._post(
            f"/applications/{uuid}/scheduled-tasks", json=_dump(model), response_model=ScheduledTask
        )

    async def update_scheduled_task(
        self, uuid: str, task_uuid: str, model: ScheduledTaskUpdate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Update a scheduled task by UUID."""
        return await self._patch(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}",
            json=_dump(model),
            response_model=ScheduledTask,
        )

    async def delete_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a scheduled task by UUID."""
        return await self._delete(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}", response_model=MessageResponse
        )

    async def scheduled_task_executions(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[ScheduledTaskExecutionList]:
        """List executions of a scheduled task."""
        return await self._get(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}/executions",
            response_model=list[ScheduledTaskExecution],
        )

    async def execute_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Execute a scheduled task now."""
        return await self._post(
            f"/applications/{uuid}/scheduled-tasks/{task_uuid}/execute",
            response_model=MessageResponse,
        )

    async def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return await self._put(
            f"/applications/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    async def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return await self._delete(
            f"/applications/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    async def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return await self._post(
            f"/applications/{uuid}/storages/{storage_uuid}/backups/run",
            response_model=MessageResponse,
        )
