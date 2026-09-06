"""Databases resource clients (sync + async)."""

from __future__ import annotations

from typing import Any

from coolipy._base import AsyncResourceBase, ResourceBase
from coolipy._response import CoolipyAPIResponse
from coolipy.exceptions import CoolipyValidationError
from coolipy.models.common import (
    BulkEnvsUpdate,
    DeploymentQueuedResponse,
    EnvironmentVariable,
    EnvironmentVariableCreate,
    EnvironmentVariableUpdate,
    Logs,
    MessageResponse,
    StorageCreate,
    StorageUpdate,
    Tag,
    TagsCreate,
    UUIDResponse,
    VolumeBackupScheduleRequest,
    VolumeBackupScheduleResponse,
)
from coolipy.models.databases import (
    ClickhouseModelCreate,
    DatabaseBackupCreate,
    DatabaseModel,
    DatabaseUpdateModel,
    DragonflyModelCreate,
    KeyDBModelCreate,
    MariaDBModelCreate,
    MongoDBModelCreate,
    MySQLModelCreate,
    PostgreSQLModelCreate,
    RedisModelCreate,
)

DatabaseList = list[DatabaseModel]
EnvironmentVariableList = list[EnvironmentVariable]
TagList = list[Tag]

_DATABASE_CREATE_PATHS: dict[type, str] = {
    PostgreSQLModelCreate: "/databases/postgresql",
    MySQLModelCreate: "/databases/mysql",
    MariaDBModelCreate: "/databases/mariadb",
    MongoDBModelCreate: "/databases/mongodb",
    RedisModelCreate: "/databases/redis",
    ClickhouseModelCreate: "/databases/clickhouse",
    DragonflyModelCreate: "/databases/dragonfly",
    KeyDBModelCreate: "/databases/keydb",
}


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


class Databases(ResourceBase):
    """Synchronous client for Coolify databases."""

    def list(self) -> CoolipyAPIResponse[DatabaseList]:
        """List all databases."""
        return self._get("/databases", response_model=list[DatabaseModel])

    def get(self, uuid: str) -> CoolipyAPIResponse[DatabaseModel]:
        """Get a database by UUID."""
        return self._get(f"/databases/{uuid}", response_model=DatabaseModel)

    def create(self, model: Any) -> CoolipyAPIResponse[Any]:
        """Create a database from one of the supported create models."""
        path = _DATABASE_CREATE_PATHS.get(type(model))
        if path is None:
            raise CoolipyValidationError(
                f"Unsupported database create model: {type(model).__name__}"
            )
        return self._post(path, json=_dump(model))

    def update(self, uuid: str, model: DatabaseUpdateModel) -> CoolipyAPIResponse[Any]:
        """Update a database by UUID."""
        return self._patch(f"/databases/{uuid}", json=_dump(model))

    def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a database by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return self._delete(f"/databases/{uuid}", params=params, response_model=MessageResponse)

    def backups(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List scheduled backups for a database."""
        return self._get(f"/databases/{uuid}/backups")

    def create_backup(self, uuid: str, model: DatabaseBackupCreate) -> CoolipyAPIResponse[dict]:
        """Create a scheduled backup configuration for a database."""
        return self._post(f"/databases/{uuid}/backups", json=_dump(model), response_model=dict)

    def update_backup(
        self, uuid: str, scheduled_backup_uuid: str, model: DatabaseBackupCreate
    ) -> CoolipyAPIResponse[Any]:
        """Update a scheduled backup configuration."""
        return self._patch(f"/databases/{uuid}/backups/{scheduled_backup_uuid}", json=_dump(model))

    def delete_backup(self, uuid: str, scheduled_backup_uuid: str) -> CoolipyAPIResponse[Any]:
        """Delete a scheduled backup configuration."""
        return self._delete(f"/databases/{uuid}/backups/{scheduled_backup_uuid}")

    def backup_executions(self, uuid: str, scheduled_backup_uuid: str) -> CoolipyAPIResponse[Any]:
        """List executions of a scheduled backup."""
        return self._get(f"/databases/{uuid}/backups/{scheduled_backup_uuid}/executions")

    def delete_backup_execution(
        self, uuid: str, scheduled_backup_uuid: str, execution_uuid: str
    ) -> CoolipyAPIResponse[Any]:
        """Delete a backup execution."""
        return self._delete(
            f"/databases/{uuid}/backups/{scheduled_backup_uuid}/executions/{execution_uuid}"
        )

    def logs(self, uuid: str) -> CoolipyAPIResponse[Logs]:
        """Get database logs."""
        return self._get(f"/databases/{uuid}/logs", response_model=Logs)

    def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move a database to another environment."""
        return self._post(
            f"/databases/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate a database to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return self._post(f"/databases/{uuid}/migrate", json=body)

    def start(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start a database."""
        return self._post(f"/databases/{uuid}/start", response_model=DeploymentQueuedResponse)

    def stop(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Stop a database."""
        return self._post(f"/databases/{uuid}/stop", response_model=MessageResponse)

    def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart a database."""
        return self._post(f"/databases/{uuid}/restart", response_model=DeploymentQueuedResponse)

    def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a database."""
        return self._get(f"/databases/{uuid}/envs", response_model=list[EnvironmentVariable])

    def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a database."""
        return self._post(f"/databases/{uuid}/envs", json=_dump(model), response_model=UUIDResponse)

    def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for a database."""
        return self._patch(
            f"/databases/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for a database."""
        return self._patch(
            f"/databases/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return self._delete(f"/databases/{uuid}/envs/{env_uuid}", response_model=MessageResponse)

    def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for a database."""
        return self._get(f"/databases/{uuid}/storages", response_model=dict)

    def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for a database."""
        return self._post(f"/databases/{uuid}/storages", json=_dump(model), response_model=dict)

    def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for a database."""
        return self._patch(f"/databases/{uuid}/storages", json=_dump(model), response_model=dict)

    def delete_storage(self, uuid: str, storage_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return self._delete(
            f"/databases/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for a database."""
        return self._get(f"/databases/{uuid}/tags", response_model=list[Tag])

    def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to a database."""
        return self._post(f"/databases/{uuid}/tags", json=_dump(model), response_model=list[Tag])

    def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from a database."""
        return self._delete(f"/databases/{uuid}/tags/{tag_uuid}")

    def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone a database into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return self._post(f"/databases/{uuid}/clone", json=body, response_model=dict)

    def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return self._put(
            f"/databases/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return self._delete(
            f"/databases/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return self._post(
            f"/databases/{uuid}/storages/{storage_uuid}/backups/run", response_model=MessageResponse
        )


class AsyncDatabases(AsyncResourceBase):
    """Asynchronous client for Coolify databases."""

    async def list(self) -> CoolipyAPIResponse[DatabaseList]:
        """List all databases."""
        return await self._get("/databases", response_model=list[DatabaseModel])

    async def get(self, uuid: str) -> CoolipyAPIResponse[DatabaseModel]:
        """Get a database by UUID."""
        return await self._get(f"/databases/{uuid}", response_model=DatabaseModel)

    async def create(self, model: Any) -> CoolipyAPIResponse[Any]:
        """Create a database from one of the supported create models."""
        path = _DATABASE_CREATE_PATHS.get(type(model))
        if path is None:
            raise CoolipyValidationError(
                f"Unsupported database create model: {type(model).__name__}"
            )
        return await self._post(path, json=_dump(model))

    async def update(self, uuid: str, model: DatabaseUpdateModel) -> CoolipyAPIResponse[Any]:
        """Update a database by UUID."""
        return await self._patch(f"/databases/{uuid}", json=_dump(model))

    async def delete(
        self,
        uuid: str,
        *,
        delete_configurations: bool = True,
        delete_volumes: bool = True,
        docker_cleanup: bool = True,
        delete_connected_networks: bool = True,
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a database by UUID."""
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        return await self._delete(
            f"/databases/{uuid}", params=params, response_model=MessageResponse
        )

    async def backups(self, uuid: str) -> CoolipyAPIResponse[Any]:
        """List scheduled backups for a database."""
        return await self._get(f"/databases/{uuid}/backups")

    async def create_backup(
        self, uuid: str, model: DatabaseBackupCreate
    ) -> CoolipyAPIResponse[dict]:
        """Create a scheduled backup configuration for a database."""
        return await self._post(
            f"/databases/{uuid}/backups", json=_dump(model), response_model=dict
        )

    async def update_backup(
        self, uuid: str, scheduled_backup_uuid: str, model: DatabaseBackupCreate
    ) -> CoolipyAPIResponse[Any]:
        """Update a scheduled backup configuration."""
        return await self._patch(
            f"/databases/{uuid}/backups/{scheduled_backup_uuid}", json=_dump(model)
        )

    async def delete_backup(self, uuid: str, scheduled_backup_uuid: str) -> CoolipyAPIResponse[Any]:
        """Delete a scheduled backup configuration."""
        return await self._delete(f"/databases/{uuid}/backups/{scheduled_backup_uuid}")

    async def backup_executions(
        self, uuid: str, scheduled_backup_uuid: str
    ) -> CoolipyAPIResponse[Any]:
        """List executions of a scheduled backup."""
        return await self._get(f"/databases/{uuid}/backups/{scheduled_backup_uuid}/executions")

    async def delete_backup_execution(
        self, uuid: str, scheduled_backup_uuid: str, execution_uuid: str
    ) -> CoolipyAPIResponse[Any]:
        """Delete a backup execution."""
        return await self._delete(
            f"/databases/{uuid}/backups/{scheduled_backup_uuid}/executions/{execution_uuid}"
        )

    async def logs(self, uuid: str) -> CoolipyAPIResponse[Logs]:
        """Get database logs."""
        return await self._get(f"/databases/{uuid}/logs", response_model=Logs)

    async def move(self, uuid: str, environment_uuid: str) -> CoolipyAPIResponse[dict]:
        """Move a database to another environment."""
        return await self._post(
            f"/databases/{uuid}/move",
            json={"environment_uuid": environment_uuid},
            response_model=dict,
        )

    async def migrate(
        self, uuid: str, destination_uuid: str, *, migrate_volumes: bool = True
    ) -> CoolipyAPIResponse[Any]:
        """Migrate a database to another destination/server."""
        body = {"destination_uuid": destination_uuid, "migrate_volumes": migrate_volumes}
        return await self._post(f"/databases/{uuid}/migrate", json=body)

    async def start(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Start a database."""
        return await self._post(f"/databases/{uuid}/start", response_model=DeploymentQueuedResponse)

    async def stop(self, uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Stop a database."""
        return await self._post(f"/databases/{uuid}/stop", response_model=MessageResponse)

    async def restart(self, uuid: str) -> CoolipyAPIResponse[DeploymentQueuedResponse]:
        """Restart a database."""
        return await self._post(
            f"/databases/{uuid}/restart", response_model=DeploymentQueuedResponse
        )

    async def envs(self, uuid: str) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """List environment variables for a database."""
        return await self._get(f"/databases/{uuid}/envs", response_model=list[EnvironmentVariable])

    async def create_env(
        self, uuid: str, model: EnvironmentVariableCreate
    ) -> CoolipyAPIResponse[UUIDResponse]:
        """Create an environment variable for a database."""
        return await self._post(
            f"/databases/{uuid}/envs", json=_dump(model), response_model=UUIDResponse
        )

    async def update_env(
        self, uuid: str, model: EnvironmentVariableUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariable]:
        """Update an environment variable for a database."""
        return await self._patch(
            f"/databases/{uuid}/envs", json=_dump(model), response_model=EnvironmentVariable
        )

    async def bulk_update_envs(
        self, uuid: str, model: BulkEnvsUpdate
    ) -> CoolipyAPIResponse[EnvironmentVariableList]:
        """Bulk-update environment variables for a database."""
        return await self._patch(
            f"/databases/{uuid}/envs/bulk",
            json=_dump(model),
            response_model=list[EnvironmentVariable],
        )

    async def delete_env(self, uuid: str, env_uuid: str) -> CoolipyAPIResponse[MessageResponse]:
        """Delete an environment variable by UUID."""
        return await self._delete(
            f"/databases/{uuid}/envs/{env_uuid}", response_model=MessageResponse
        )

    async def storages(self, uuid: str) -> CoolipyAPIResponse[dict]:
        """List storages for a database."""
        return await self._get(f"/databases/{uuid}/storages", response_model=dict)

    async def create_storage(self, uuid: str, model: StorageCreate) -> CoolipyAPIResponse[dict]:
        """Create a storage for a database."""
        return await self._post(
            f"/databases/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def update_storage(self, uuid: str, model: StorageUpdate) -> CoolipyAPIResponse[dict]:
        """Update a storage for a database."""
        return await self._patch(
            f"/databases/{uuid}/storages", json=_dump(model), response_model=dict
        )

    async def delete_storage(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Delete a storage by UUID."""
        return await self._delete(
            f"/databases/{uuid}/storages/{storage_uuid}", response_model=MessageResponse
        )

    async def tags(self, uuid: str) -> CoolipyAPIResponse[TagList]:
        """List tags for a database."""
        return await self._get(f"/databases/{uuid}/tags", response_model=list[Tag])

    async def add_tags(self, uuid: str, model: TagsCreate) -> CoolipyAPIResponse[TagList]:
        """Add one or more tags to a database."""
        return await self._post(
            f"/databases/{uuid}/tags", json=_dump(model), response_model=list[Tag]
        )

    async def delete_tag(self, uuid: str, tag_uuid: str) -> CoolipyAPIResponse[Any]:
        """Remove a tag from a database."""
        return await self._delete(f"/databases/{uuid}/tags/{tag_uuid}")

    async def clone(
        self,
        uuid: str,
        destination_uuid: str,
        *,
        name: str | None = None,
        clone_volumes: bool = False,
    ) -> CoolipyAPIResponse[dict]:
        """Clone a database into a destination."""
        body = {"destination_uuid": destination_uuid, "name": name, "clone_volumes": clone_volumes}
        return await self._post(f"/databases/{uuid}/clone", json=body, response_model=dict)

    async def update_storage_backup(
        self, uuid: str, storage_uuid: str, model: VolumeBackupScheduleRequest
    ) -> CoolipyAPIResponse[VolumeBackupScheduleResponse]:
        """Schedule backups for a storage volume."""
        return await self._put(
            f"/databases/{uuid}/storages/{storage_uuid}/backups",
            json=_dump(model),
            response_model=VolumeBackupScheduleResponse,
        )

    async def delete_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Remove the backup schedule for a storage volume."""
        return await self._delete(
            f"/databases/{uuid}/storages/{storage_uuid}/backups", response_model=MessageResponse
        )

    async def run_storage_backup(
        self, uuid: str, storage_uuid: str
    ) -> CoolipyAPIResponse[MessageResponse]:
        """Run a storage backup now."""
        return await self._post(
            f"/databases/{uuid}/storages/{storage_uuid}/backups/run", response_model=MessageResponse
        )
