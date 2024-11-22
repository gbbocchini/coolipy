from dataclasses import asdict
import json
from typing import Union
from constants import COOLIFY_RETURN_TYPES, URL_MAP
from exceptions import CoolipyAPIServiceException
from models.coolify_api_response import CoolifyAPIResponse
from models.databases import (
    ClickHouseModelCreate,
    DatabaseModel,
    DatabaseUpdateModel,
    DragonFlyModelCreate,
    KeyDBModelCreate,
    MariaDBModelCreate,
    MongoDBModelCreate,
    MySQLModelCreate,
    PostgreSQLModelCreate,
    RedisModelCreate,
    DATABASE_TYPES_MAP,
)
from services.coolify_api.base import CoolifyApiBase


class Databases(CoolifyApiBase):
    """
    Provides methods for managing databases via the Coolify API.
    """
    def list(self) -> CoolifyAPIResponse:
        """
        Retrieves a list of all databases.

        Returns:
            CoolifyAPIResponse: Response containing a list of databases.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(content, COOLIFY_RETURN_TYPES.list, DatabaseModel)

    def get(self, database_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieves details of a specific database.

        Args:
            database_uuid: Unique identifier of the database.

        Returns:
            CoolifyAPIResponse: Response containing database details.
        """
        content = self._http.get(f"{self._base_url}/{database_uuid}")
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.single, DatabaseModel
        )

    def delete(
        self,
        database_uuid: str,
        delete_configurations: bool,
        delete_volumes: bool,
        docker_cleanup: bool,
        delete_connected_networks: bool,
    ) -> CoolifyAPIResponse:
        """
        Deletes a specific database with configurable options.

        Args:
            database_uuid: Unique identifier of the database.
            delete_configurations: Whether to delete configuration files.
            delete_volumes: Whether to delete data volumes.
            docker_cleanup: Whether to perform Docker cleanup.
            delete_connected_networks: Whether to delete connected networks.

        Returns:
            CoolifyAPIResponse: Raw response indicating the deletion status.
        """
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        query_p = self._build_url_params_from_dict(params)
        content = self._http.delete(f"{self._base_url}/{database_uuid}?{query_p}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def create(
        self,
        database_model_create: Union[
            PostgreSQLModelCreate,
            ClickHouseModelCreate,
            DragonFlyModelCreate,
            RedisModelCreate,
            KeyDBModelCreate,
            MariaDBModelCreate,
            MySQLModelCreate,
            MongoDBModelCreate,
        ],
    ) -> CoolifyAPIResponse:
        """
        Creates a new database using the specified model.

        Args:
            database_model_create: The database creation model to use.

        Returns:
            CoolifyAPIResponse: Response containing the created database.
        """
        url_complement = self._infer_url_sufix_from_model(
            database_model_create, DATABASE_TYPES_MAP
        )
        db_as_dict = asdict(database_model_create)
        content = self._http.post(
            f"{self._base_url}/{url_complement}", data=json.dumps(db_as_dict)
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.single, DatabaseModel)

    def update(self, database_uuid: str, database_model_update: DatabaseUpdateModel) -> CoolifyAPIResponse:
        """
        Updates an existing database with new data.

        Args:
            database_uuid: Unique identifier of the database.
            database_model_update: Updated database model.

        Returns:
            CoolifyAPIResponse: Raw response indicating the update status.
        """
        as_dict = asdict(database_model_update)
        content = self._http.patch(
            f"{self._base_url}/{database_uuid}", data=json.dumps(as_dict)
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)


    def start(self, database_uuid: str) -> CoolifyAPIResponse:
        """
        Starts a specific database.

        Args:
            database_uuid: Unique identifier of the database.

        Returns:
            CoolifyAPIResponse: Raw response indicating the start status.
        """
        content = self._http.get(f"{self._base_url}/{database_uuid}{URL_MAP.start}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def stop(self, database_uuid: str) -> CoolifyAPIResponse:
        """
        Stops a specific database.

        Args:
            database_uuid: Unique identifier of the database.

        Returns:
            CoolifyAPIResponse: Raw response indicating the stop status.
        """
        content = self._http.get(f"{self._base_url}/{database_uuid}{URL_MAP.stop}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def restart(self, database_uuid: str) -> CoolifyAPIResponse:
        """
        Restarts a specific database.

        Args:
            database_uuid: Unique identifier of the database.

        Returns:
            CoolifyAPIResponse: Raw response indicating the restart status.
        """
        content = self._http.get(f"{self._base_url}/{database_uuid}{URL_MAP.restart}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)
