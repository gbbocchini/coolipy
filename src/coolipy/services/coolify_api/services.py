from dataclasses import asdict
import json
from typing import List
from coolipy.constants import COOLIFY_RETURN_TYPES, URL_MAP
from coolipy.models.env_vars import EnvVarModel, EnvVarModelsCreate
from coolipy.services.coolify_api.base import CoolifyApiBase
from coolipy.models.coolify_api_response import CoolifyAPIResponse
from coolipy.models.service import ServiceModel, ServiceModelCreate


class Services(CoolifyApiBase):
    """
    Handles operations for managing services in Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Fetches the list of services.

        Returns:
            CoolifyAPIResponse: The response containing the list of services.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.list, model=ServiceModel
        )

    def create(self, service: ServiceModelCreate) -> CoolifyAPIResponse:
        """
        Creates a new service.

        Args:
            service (ServiceModelCreate): The model containing the service data to create.

        Returns:
            CoolifyAPIResponse: The response containing the created service data.
        """
        model_as_dict = asdict(service)
        content = self._http.post(self._base_url, data=json.dumps(model_as_dict))
        return self._handle_response(content, COOLIFY_RETURN_TYPES.single, ServiceModel)

    def get(self, service_uuid: str) -> CoolifyAPIResponse:
        """
        Fetches a specific service by UUID.

        Args:
            service_uuid (str): The UUID of the service to fetch.

        Returns:
            CoolifyAPIResponse: The response containing the service data.
        """
        content = self._http.get(f"{self._base_url}/{service_uuid}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.single, ServiceModel)

    def delete(
        self,
        service_uuid: str,
        delete_configurations: bool,
        delete_volumes: bool,
        docker_cleanup: bool,
        delete_connected_networks: bool,
    ) -> CoolifyAPIResponse:
        """
        Deletes a service with specified cleanup options.

        Args:
            service_uuid (str): The UUID of the service to delete.
            delete_configurations (bool): Whether to delete the configurations.
            delete_volumes (bool): Whether to delete the volumes.
            docker_cleanup (bool): Whether to clean up Docker.
            delete_connected_networks (bool): Whether to delete connected networks.

        Returns:
            CoolifyAPIResponse: The response after deleting the service.
        """
        params = {
            "delete_configurations": delete_configurations,
            "delete_volumes": delete_volumes,
            "docker_cleanup": docker_cleanup,
            "delete_connected_networks": delete_connected_networks,
        }
        query_p = self._build_url_params_from_dict(params)
        content = self._http.delete(f"{self._base_url}/{service_uuid}?{query_p}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def list_envs(self, service_uuid: str) -> CoolifyAPIResponse:
        """
        Fetches environment variables for a service.

        Args:
            service_uuid (str): The UUID of the service to fetch environment variables for.

        Returns:
            CoolifyAPIResponse: The response containing the list of environment variables.
        """
        content = self._http.get(f"{self._base_url}/{service_uuid}{URL_MAP.envs}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.list, EnvVarModel)

    def create_env(
        self, service_uuid: str, env_var: EnvVarModelsCreate
    ) -> CoolifyAPIResponse:
        """
        Creates a new environment variable for a service.

        Args:
            service_uuid (str): The UUID of the service to add the environment variable to.
            env_var (EnvVarModelsCreate): The environment variable data to create.

        Returns:
            CoolifyAPIResponse: The response containing the created environment variable.
        """
        env_as_dict = asdict(env_var)
        content = self._http.post(
            f"{self._base_url}/{service_uuid}/envs", data=json.dumps(env_as_dict)
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.single, EnvVarModel)

    def update_env(
        self, service_uuid: str, env_var_updated: EnvVarModelsCreate
    ) -> CoolifyAPIResponse:
        """
        Updates an environment variable for a service.

        Args:
            service_uuid (str): The UUID of the service to update the environment variable for.
            env_var_updated (EnvVarModelCreate): The updated environment variable data.

        Returns:
            CoolifyAPIResponse: The response containing the updated environment variable.
        """
        env_as_dict = asdict(env_var_updated)
        content = self._http.patch(
            f"{self._base_url}/{service_uuid}{URL_MAP.envs}",
            data=json.dumps(env_as_dict),
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def bulk_update_env(
        self, service_uuid: str, env_vars_updated: List[EnvVarModelsCreate]
    ) -> CoolifyAPIResponse:
        """
        Bulk updates environment variables for a service.

        Args:
            service_uuid (str): The UUID of the service to update the environment variables for.
            env_vars_updated (List[EnvVarModelsCreate]): The list of updated environment variable data.

        Returns:
            CoolifyAPIResponse: The response after bulk updating the environment variables.
        """
        envs_as_dict = [asdict(i) for i in env_vars_updated]
        content = self._http.patch(
            f"{self._base_url}/{service_uuid}{URL_MAP.envs}{URL_MAP.bulk}",
            data=json.dumps(envs_as_dict),
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def delete_env(self, service_uuid: str, env_uuid: str) -> CoolifyAPIResponse:
        """
        Deletes an environment variable from a service.

        Args:
            service_uuid (str): The UUID of the service to delete the environment variable from.
            env_uuid (str): The UUID of the environment variable to delete.

        Returns:
            CoolifyAPIResponse: The response after deleting the environment variable.
        """
        content = self._http.delete(
            f"{self._base_url}/{service_uuid}{URL_MAP.envs}/{env_uuid}"
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def start(self, service_uuid: str) -> CoolifyAPIResponse:
        """
        Starts a service.

        Args:
            service_uuid (str): The UUID of the service to start.

        Returns:
            CoolifyAPIResponse: The response after starting the service.
        """
        content = self._http.get(f"{self._base_url}/{service_uuid}{URL_MAP.start}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def stop(self, service_uuid: str) -> CoolifyAPIResponse:
        """
        Stops a service.

        Args:
            service_uuid (str): The UUID of the service to stop.

        Returns:
            CoolifyAPIResponse: The response after stopping the service.
        """
        content = self._http.get(f"{self._base_url}/{service_uuid}{URL_MAP.stop}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def restart(self, service_uuid: str) -> CoolifyAPIResponse:
        """
        Restarts a service.

        Args:
            service_uuid (str): The UUID of the service to restart.

        Returns:
            CoolifyAPIResponse: The response after restarting the service.
        """
        content = self._http.get(f"{self._base_url}/{service_uuid}{URL_MAP.restart}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)
