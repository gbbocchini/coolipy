from typing import List, Optional
from constants import COOLIFY_RETURN_TYPES, URL_MAP
from models.coolify_api_response import CoolifyAPIResponse
from .base import CoolifyApiBase
from models.deployments import DeploymentsModel


class Deployments(CoolifyApiBase):
    """
    Manages deployments in the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieve a list of all deployments.

        Returns:
            CoolifyAPIResponse: The API response containing a list of
            deployments as instances of `DeploymentsModel`.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.list, model=DeploymentsModel
        )

    def get(self, deployment_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve details of a specific deployment.

        Args:
            deployment_uuid (str): The unique identifier of the deployment to retrieve.

        Returns:
            CoolifyAPIResponse: The API response containing the deployment details
            as an instance of `DeploymentsModel`.
        """
        content = self._http.get(f"{self._base_url}/{deployment_uuid}")
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.single, model=DeploymentsModel
        )

    def deploy(
        self, resource_uuid: str, tag: Optional[str] = None, force: bool = False
    ) -> CoolifyAPIResponse:
        """
        Initiates a deployment for a specific resource.

        Args:
            resource_uuid: Unique identifier of the resource to deploy.
            tag: Optional tag to specify the deployment version.
            force: Whether to force the deployment.

        Returns:
            CoolifyAPIResponse: Response containing the deployment result.
        """
        params = {"uuid": resource_uuid, "tag": tag if tag else "", "force": force}
        query_p = self._build_url_params_from_dict(params)
        content = self._http.get(f"{URL_MAP.deploy}?{query_p}")
        return self._handle_response(
            content, COOLIFY_RETURN_TYPES.list, DeploymentsModel
        )
