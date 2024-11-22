import json
from models.coolify_api_response import CoolifyAPIResponse
from services.coolify_api.base import CoolifyApiBase
from constants import COOLIFY_RETURN_TYPES

from models.projects import ProjectsModel
from models.environs import EnvironmentsModel


class Projects(CoolifyApiBase):
    """
    Handles operations related to projects in the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieve all projects.

        Returns:
            CoolifyAPIResponse: Response containing a list of projects.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.list, model=ProjectsModel
        )

    def get(self, project_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve a project by UUID.

        Args:
            project_uuid (str): The UUID of the project.

        Returns:
            CoolifyAPIResponse: Response containing the project details.
        """
        content = self._http.get(f"{self._base_url}/{project_uuid}")
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.single, model=ProjectsModel
        )

    def update(
        self, project_uuid: str, project_updated_description: str
    ) -> CoolifyAPIResponse:
        """
        Update the description of a project.

        Args:
            project_uuid (str): The UUID of the project.
            project_updated_description (str): The new description for the project.

        Returns:
            CoolifyAPIResponse: Response from the API after updating the project.
        """
        resp = self._http.patch(
            f"{self._base_url}/{project_uuid}",
            data=json.dumps({"description": project_updated_description}),
        )
        return self._handle_response(
            resp, return_type=COOLIFY_RETURN_TYPES.single, model=ProjectsModel
        )

    def delete(self, project_uuid: str) -> CoolifyAPIResponse:
        """
        Delete a project by UUID.

        Args:
            project_uuid (str): The UUID of the project.

        Returns:
            CoolifyAPIResponse: Response from the API after deletion.
        """
        resp = self._http.delete(f"{self._base_url}/{project_uuid}")
        return self._handle_response(resp, return_type=COOLIFY_RETURN_TYPES.raw)

    def environment(
        self, project_uuid: str, environment_name: str
    ) -> CoolifyAPIResponse:
        """
        Retrieve environment details for a specific project.

        Args:
            project_uuid (str): The UUID of the project.
            environment_name (str): The name of the environment.

        Returns:
            CoolifyAPIResponse: Response containing the environment details.
        """
        resp = self._http.get(f"{self._base_url}/{project_uuid}/{environment_name}")
        return self._handle_response(
            resp, return_type=COOLIFY_RETURN_TYPES.single, model=EnvironmentsModel
        )

    def create(self, project_name: str, project_description: str) -> CoolifyAPIResponse:
        """
        Create a new project.

        Args:
            project_name (str): The name of the new project.
            project_description (str): The description of the new project.

        Returns:
            CoolifyAPIResponse: Response containing the created project details.
        """
        post_data = json.dumps(
            {"name": project_name, "description": project_description}
        )
        resp = self._http.post(self._base_url, data=post_data)
        return self._handle_response(
            resp, return_type=COOLIFY_RETURN_TYPES.single, model=ProjectsModel
        )
