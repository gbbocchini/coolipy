"""Services resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
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
from coolipy.models.services import ServiceCreateModel, ServiceModel, ServiceUpdateModel

ServiceList = list[ServiceModel]
EnvironmentVariableList = list[EnvironmentVariable]
ScheduledTaskList = list[ScheduledTask]
ScheduledTaskExecutionList = list[ScheduledTaskExecution]
TagList = list[Tag]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Services(ResourceBase):
    """Synchronous client for Coolify services."""

    def list(self) -> CoolipyAPIResponse[ServiceList]:
        """List all services."""
        return self._get("/services", response_model=list[ServiceModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[ServiceModel]:
        """Get a service by UUID."""
        return self._get(f"/services/{uuid}", response_model=ServiceModel)

    def create(self, model: ServiceCreateModel) -> CoolipyAPIResponse[dict]:
        """Create a service."""
        return self._post("/services", json=_dump(model), response_model=dict)

    def update(self, uuid: str, model: ServiceUpdateModel) -> CoolipyAPIResponse[dict]:
        """Update a service by UUID."""
        return self._patch(f"/services/{uuid}", json=_dump(model), response_model=dict)

    def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a service by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return self._delete(f"/services/{uuid}", params=params, response_model=MessageResponse)

    def logs(self, uuid: str) -> CoolipyAPIResponse[Logs]:
        """Get service logs."""
        return self._get(f"/services/{uuid}/logs", response_model=Logs)

    def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a service."""
        return self._get(f"/services/{uuid}/envs", response_model=list[EnvironmentVariable])

    def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a service."""
        return self._post(f"/services/{uuid}/envs", json=_dump(model), response_model=UUIDResponse)

    def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for a service."""
        return self._patch(
            f"/services/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for a service."""
        return self._patch(
            f"/services/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return self._delete(f"/services/{uuid}/envs/{env_uuid}", response_model=MessageResponse)

    def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move a service to another environment."""
        return self._post(
            f"/services/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate a service to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return self._post(f"/services/{uuid}/migrate", json=body)

    def start(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start a service."""
        return self._post(f"/services/{uuid}/start", response_model=DeploymentQueuedResponse)

    def stop(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Stop a service."""
        return self._post(f"/services/{uuid}/stop", response_model=MessageResponse)

    def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart a service."""
        return self._post(f"/services/{uuid}/restart", response_model=DeploymentQueuedResponse)

    def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for a service."""
        return self._get(f"/services/{uuid}/storages", response_model=dict)

    def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for a service."""
        return self._post(f"/services/{uuid}/storages", json=_dump(model), response_model=dict)

    def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for a service."""
        return self._patch(f"/services/{uuid}/storages", json=_dump(model), response_model=dict)

    def delete_storage(self, uuid: str, storage_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return self._delete(
            f"/services/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for a service."""
        return self._get(f"/services/{uuid}/tags", response_model=list[Tag])

    def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to a service."""
        return self._post(f"/services/{uuid}/tags", json=_dump(model), response_model=list[Tag])

    def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from a service."""
        return self._delete(f"/services/{uuid}/tags/{tag_uuid}")

    def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone a service into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return self._post(f"/services/{uuid}/clone", json=body, response_model=dict)

    def scheduled_tasks(self, uuid: str) -> CoolipyAPIResponse[ScheduledTaskList]:
        """List scheduled tasks for a service."""
        return self._get(f"/services/{uuid}/scheduled-tasks", response_model=list[ScheduledTask])

    def create_scheduled_task(
        self, uuid: str, model: ScheduledTaskCreate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Create a scheduled task for a service."""
        return self._post(
            f"/services/{uuid}/scheduled-tasks", json=_dump(model), response_model=ScheduledTask
        )

    def update_scheduled_task(
        self, uuid: str, task_uuid: str, model: ScheduledTaskUpdate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Update a scheduled task by UUID."""
        return self._patch(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}",
            json=_dump(model),
            response_model=ScheduledTask,
        )

    def delete_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a scheduled task by UUID."""
        return self._delete(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}", response_model=MessageResponse
        )

    def scheduled_task_executions(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[ScheduledTaskExecutionList]:
        """List executions of a scheduled task."""
        return self._get(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}/executions",
            response_model=list[ScheduledTaskExecution],
        )

    def execute_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Execute a scheduled task now."""
        return self._post(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}/execute", response_model=MessageResponse
        )

    def applications(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List applications belonging to a service."""
        return self._get(f"/services/{uuid}/applications")

    def get_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get a service application by UUID."""
        return self._get(f"/services/{uuid}/applications/{app_uuid}")

    def update_application(self, uuid: str, app_uuid: str, model: Any) -> CoolipyAPIResponse[Any]:
        """Update a service application."""
        return self._patch(f"/services/{uuid}/applications/{app_uuid}", json=_dump(model))

    def application_logs(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get service application logs."""
        return self._get(f"/services/{uuid}/applications/{app_uuid}/logs")

    def start_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Start a service application."""
        return self._post(f"/services/{uuid}/applications/{app_uuid}/start")

    def restart_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Restart a service application."""
        return self._post(f"/services/{uuid}/applications/{app_uuid}/restart")

    def stop_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Stop a service application."""
        return self._post(f"/services/{uuid}/applications/{app_uuid}/stop")

    def databases(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List databases belonging to a service."""
        return self._get(f"/services/{uuid}/databases")

    def get_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get a service database by UUID."""
        return self._get(f"/services/{uuid}/databases/{database_uuid}")

    def update_database(self, uuid: str, database_uuid: str, model: Any) -> CoolipyAPIResponse[Any]:
        """Update a service database."""
        return self._patch(f"/services/{uuid}/databases/{database_uuid}", json=_dump(model))

    def database_logs(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get service database logs."""
        return self._get(f"/services/{uuid}/databases/{database_uuid}/logs")

    def start_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Start a service database."""
        return self._post(f"/services/{uuid}/databases/{database_uuid}/start")

    def restart_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Restart a service database."""
        return self._post(f"/services/{uuid}/databases/{database_uuid}/restart")

    def stop_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Stop a service database."""
        return self._post(f"/services/{uuid}/databases/{database_uuid}/stop")

    def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return self._put(
            f"/services/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return self._delete(
            f"/services/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return self._post(
            f"/services/{uuid}/storages/{storage_uuid}/backups/run", response_model=MessageResponse
        )


class AsyncServices(AsyncResourceBase):
    """Asynchronous client for Coolify services."""

    async def list(self) -> CoolipyAPIResponse[ServiceList]:
        """List all services."""
        return await self._get("/services", response_model=list[ServiceModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[ServiceModel]:
        """Get a service by UUID."""
        return await self._get(f"/services/{uuid}", response_model=ServiceModel)

    async def create(self, model: ServiceCreateModel) -> CoolipyAPIResponse[dict]:
        """Create a service."""
        return await self._post("/services", json=_dump(model), response_model=dict)

    async def update(self, uuid: str, model: ServiceUpdateModel) -> CoolipyAPIResponse[dict]:
        """Update a service by UUID."""
        return await self._patch(f"/services/{uuid}", json=_dump(model), response_model=dict)

    async def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a service by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return await self._delete(
            f"/services/{uuid}", params=params, response_model=MessageResponse
        )

    async def logs(self, uuid: str) -> CoolipyAPIResponse[Logs]:
        """Get service logs."""
        return await self._get(f"/services/{uuid}/logs", response_model=Logs)

    async def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a service."""
        return await self._get(f"/services/{uuid}/envs", response_model=list[EnvironmentVariable])

    async def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a service."""
        return await self._post(
            f"/services/{uuid}/envs", json=_dump(model), response_model=UUIDResponse
        )

    async def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for a service."""
        return await self._patch(
            f"/services/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    async def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for a service."""
        return await self._patch(
            f"/services/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    async def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return await self._delete(
            f"/services/{uuid}/envs/{env_uuid}", response_model=MessageResponse
        )

    async def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move a service to another environment."""
        return await self._post(
            f"/services/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    async def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate a service to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return await self._post(f"/services/{uuid}/migrate", json=body)

    async def start(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start a service."""
        return await self._post(f"/services/{uuid}/start", response_model=DeploymentQueuedResponse)

    async def stop(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Stop a service."""
        return await self._post(f"/services/{uuid}/stop", response_model=MessageResponse)

    async def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart a service."""
        return await self._post(
            f"/services/{uuid}/restart", response_model=DeploymentQueuedResponse
        )

    async def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for a service."""
        return await self._get(f"/services/{uuid}/storages", response_model=dict)

    async def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for a service."""
        return await self._post(
            f"/services/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for a service."""
        return await self._patch(
            f"/services/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def delete_storage(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return await self._delete(
            f"/services/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    async def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for a service."""
        return await self._get(f"/services/{uuid}/tags", response_model=list[Tag])

    async def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to a service."""
        return await self._post(
            f"/services/{uuid}/tags", json=_dump(model), response_model=list[Tag]
        )

    async def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from a service."""
        return await self._delete(f"/services/{uuid}/tags/{tag_uuid}")

    async def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone a service into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return await self._post(f"/services/{uuid}/clone", json=body, response_model=dict)

    async def scheduled_tasks(self, uuid: str) -> CoolipyAPIResponse[ScheduledTaskList]:
        """List scheduled tasks for a service."""
        return await self._get(
            f"/services/{uuid}/scheduled-tasks", response_model=list[ScheduledTask]
        )

    async def create_scheduled_task(
        self, uuid: str, model: ScheduledTaskCreate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Create a scheduled task for a service."""
        return await self._post(
            f"/services/{uuid}/scheduled-tasks", json=_dump(model), response_model=ScheduledTask
        )

    async def update_scheduled_task(
        self, uuid: str, task_uuid: str, model: ScheduledTaskUpdate
    ) -> CoolipyAPIResponse[ScheduledTask]:
        """Update a scheduled task by UUID."""
        return await self._patch(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}",
            json=_dump(model),
            response_model=ScheduledTask,
        )

    async def delete_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a scheduled task by UUID."""
        return await self._delete(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}", response_model=MessageResponse
        )

    async def scheduled_task_executions(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[ScheduledTaskExecutionList]:
        """List executions of a scheduled task."""
        return await self._get(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}/executions",
            response_model=list[ScheduledTaskExecution],
        )

    async def execute_scheduled_task(
        self, uuid: str, task_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Execute a scheduled task now."""
        return await self._post(
            f"/services/{uuid}/scheduled-tasks/{task_uuid}/execute", response_model=MessageResponse
        )

    async def applications(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List applications belonging to a service."""
        return await self._get(f"/services/{uuid}/applications")

    async def get_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get a service application by UUID."""
        return await self._get(f"/services/{uuid}/applications/{app_uuid}")

    async def update_application(
        self, uuid: str, app_uuid: str, model: Any
    ) -> CoolipyAPIResponse[Any]:
        """Update a service application."""
        return await self._patch(f"/services/{uuid}/applications/{app_uuid}", json=_dump(model))

    async def application_logs(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get service application logs."""
        return await self._get(f"/services/{uuid}/applications/{app_uuid}/logs")

    async def start_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Start a service application."""
        return await self._post(f"/services/{uuid}/applications/{app_uuid}/start")

    async def restart_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Restart a service application."""
        return await self._post(f"/services/{uuid}/applications/{app_uuid}/restart")

    async def stop_application(self, uuid: str, app_uuid: str) -> CoolipyAPIResponse[Any]:
        """Stop a service application."""
        return await self._post(f"/services/{uuid}/applications/{app_uuid}/stop")

    async def databases(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List databases belonging to a service."""
        return await self._get(f"/services/{uuid}/databases")

    async def get_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get a service database by UUID."""
        return await self._get(f"/services/{uuid}/databases/{database_uuid}")

    async def update_database(
        self, uuid: str, database_uuid: str, model: Any
    ) -> CoolipyAPIResponse[Any]:
        """Update a service database."""
        return await self._patch(f"/services/{uuid}/databases/{database_uuid}", json=_dump(model))

    async def database_logs(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Get service database logs."""
        return await self._get(f"/services/{uuid}/databases/{database_uuid}/logs")

    async def start_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Start a service database."""
        return await self._post(f"/services/{uuid}/databases/{database_uuid}/start")

    async def restart_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Restart a service database."""
        return await self._post(f"/services/{uuid}/databases/{database_uuid}/restart")

    async def stop_database(self, uuid: str, database_uuid: str) -> CoolipyAPIResponse[Any]:
        """Stop a service database."""
        return await self._post(f"/services/{uuid}/databases/{database_uuid}/stop")

    async def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return await self._put(
            f"/services/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    async def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return await self._delete(
            f"/services/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    async def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return await self._post(
            f"/services/{uuid}/storages/{storage_uuid}/backups/run", response_model=MessageResponse
        )
