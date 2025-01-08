from dataclasses import asdict
import json
from typing import List, Union
from coolipy.constants import COOLIFY_RETURN_TYPES, URL_MAP
from coolipy.models.applications import (
    APPLICATION_MODELS_URL_CREATE_MAP,
    ApplicationDockerComposeModelCreate,
    ApplicationDockerImageModelCreate,
    ApplicationDockerfileModelCreate,
    ApplicationModel,
    ApplicationPrivateGHModelCreate,
    ApplicationPublicModelCreate,
    ApplicationPublicPrivatePvtKeyGHModelCreate,
)
from coolipy.models.env_vars import EnvVarModel, EnvVarModelsCreate
from coolipy.services.coolify_api.base import CoolifyApiBase
from coolipy.models.coolify_api_response import CoolifyAPIResponse


class Applications(CoolifyApiBase):
    """
    Provides methods for managing applications via the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieves a list of all applications.

        Returns:
            CoolifyAPIResponse: Response containing a list of applications.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.list, ApplicationModel
        )

    def create(
        self,
        model: Union[
            ApplicationPublicModelCreate,
            ApplicationPrivateGHModelCreate,
            ApplicationPublicPrivatePvtKeyGHModelCreate,
            ApplicationDockerfileModelCreate,
            ApplicationDockerImageModelCreate,
            ApplicationDockerComposeModelCreate,
        ],
    ) -> CoolifyAPIResponse:
        """
        Creates a new application using the specified model.

        Args:
            model: The application creation model to use.

        Returns:
            CoolifyAPIResponse: Response containing the created application.
        """
        url_complement = self._infer_url_sufix_from_model(
            model, APPLICATION_MODELS_URL_CREATE_MAP
        )
        model_as_dict = asdict(model)
        content = self._http.post(
            f"{self._base_url}/{url_complement}", data=json.dumps(model_as_dict)
        )
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.single, ApplicationModel
        )

    def get(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieves details of a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Response containing application details.
        """
        content = self._http.get(f"{self._base_url}/{application_uuid}")
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.single, ApplicationModel
        )

    def delete(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Deletes a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Raw response indicating the deletion status.
        """
        content = self._http.delete(f"{self._base_url}/{application_uuid}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def update(
        self, application_uuid: str, model: ApplicationModel
    ) -> CoolifyAPIResponse:
        """
        Updates an existing application with new data.

        Args:
            application_uuid: Unique identifier of the application.
            model: Updated application model.

        Returns:
            CoolifyAPIResponse: Response containing the updated application.
        """
        model_as_dict = asdict(model)
        content = self._http.patch(
            f"{self._base_url}/{application_uuid}", data=json.dumps(model_as_dict)
        )
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.single, ApplicationModel
        )

    def list_envs(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieves environment variables for a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Response containing a list of environment variables.
        """
        content = self._http.get(f"{self._base_url}/{application_uuid}{URL_MAP.envs}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.list, EnvVarModel)

    def create_env(
        self, application_uuid: str, model: EnvVarModelsCreate
    ) -> CoolifyAPIResponse:
        """
        Retrieves environment variables for a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Response containing a list of environment variables.
        """
        model_as_dict = asdict(model)
        content = self._http.post(
            f"{self._base_url}/{application_uuid}{URL_MAP.envs}",
            data=json.dumps(model_as_dict),
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.single, EnvVarModel)

    def update_env(
        self, application_uuid: str, env_var_updated: EnvVarModelsCreate
    ) -> CoolifyAPIResponse:
        """
        Updates an existing environment variable.

        Args:
            application_uuid: Unique identifier of the application.
            env_var_updated: Updated environment variable model.

        Returns:
            CoolifyAPIResponse: Raw response indicating the update status.
        """
        env_as_dict = asdict(env_var_updated)
        content = self._http.patch(
            f"{self._base_url}/{application_uuid}{URL_MAP.envs}",
            data=json.dumps(env_as_dict),
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def bulk_update_env(
        self, application_uuid: str, env_vars_updated: List[EnvVarModelsCreate]
    ) -> CoolifyAPIResponse:
        """
        Performs a bulk update of environment variables for a specific application.

        Args:
            application_uuid: Unique identifier of the application.
            env_vars_updated: List of updated environment variable models.

        Returns:
            CoolifyAPIResponse: Raw response indicating the bulk update status.
        """
        envs_as_dict = [asdict(i) for i in env_vars_updated]
        content = self._http.patch(
            f"{self._base_url}/{application_uuid}{URL_MAP.envs}{URL_MAP.bulk}",
            data=json.dumps(envs_as_dict),
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def delete_env(self, application_uuid: str, env_uuid: str) -> CoolifyAPIResponse:
        """
        Deletes a specific environment variable from an application.

        Args:
            application_uuid: Unique identifier of the application.
            env_uuid: Unique identifier of the environment variable.

        Returns:
            CoolifyAPIResponse: Raw response indicating the deletion status.
        """
        content = self._http.delete(
            f"{self._base_url}/{application_uuid}{URL_MAP.envs}/{env_uuid}"
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def start(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Starts a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Raw response indicating the start status.
        """
        content = self._http.get(f"{self._base_url}/{application_uuid}{URL_MAP.start}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def stop(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Stops a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Raw response indicating the stop status.
        """
        content = self._http.get(f"{self._base_url}/{application_uuid}{URL_MAP.stop}")
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def restart(self, application_uuid: str) -> CoolifyAPIResponse:
        """
        Restarts a specific application.

        Args:
            application_uuid: Unique identifier of the application.

        Returns:
            CoolifyAPIResponse: Raw response indicating the restart status.
        """
        content = self._http.get(
            f"{self._base_url}/{application_uuid}{URL_MAP.restart}"
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)

    def execute_command(
        self, application_uuid: str, command: str
    ) -> CoolifyAPIResponse:
        """
        Executes a command in a specific application.

        Args:
            application_uuid: Unique identifier of the application.
            command: The command to execute.

        Returns:
            CoolifyAPIResponse: Raw response indicating the command execution status.
        """
        payload = json.dumps({"command": command})
        content = self._http.post(
            f"{self._base_url}/{application_uuid}{URL_MAP.execute}", data=payload
        )
        return self._handle_response(content, COOLIFY_RETURN_TYPES.raw)
