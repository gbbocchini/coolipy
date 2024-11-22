from dataclasses import asdict
from typing import Any, Dict, Optional, Union
from constants import COOLIFY_RETURN_TYPES
from exceptions import CoolipyAPIServiceException
from models.environs import EnvironmentsModel
from models.private_keys import PrivateKeysModel
from models.teams import TeamMemberModel, TeamModel
from services.http_service import HttpService
from models.deployments import DeploymentsModel
from models.coolify_api_response import CoolifyAPIResponse
from models.projects import ProjectsModel
from models.resources import ResourceModel
from models.servers import ServerModel


class CoolifyApiBase:
    """
    Base class for services interacting with the Coolify API, handling common logic for HTTP requests and responses.
    """

    def __init__(self, http_service: HttpService, base_service_url: str):
        """
        Initializes the Coolify API service with an HTTP service instance and a specific service URL.

        Args:
            http_service (HttpService): Instance of the HttpService class for making HTTP requests.
            base_service_url (str): The endpoint URL for the specific service (e.g., '/servers', '/teams').
        """
        self._http = http_service
        self._base_url = base_service_url

    def _build_url_params_from_dict(self, params_dict: Dict[str, Any]) -> str:
        """
        Constructs a URL query string from a dictionary of parameters.

        Args:
            params_dict: Dictionary containing key-value pairs for URL parameters.

        Returns:
            str: URL query string.
        """
        return "&".join([f"{k}={v}" for k, v in params_dict.items()])

    def _infer_url_sufix_from_model(self, model, model_map):
        """
        Determines the URL suffix based on the provided model type.

        Args:
            model: The model instance to check.
            model_map: Dictionary mapping model types to URL suffixes.

        Returns:
            str: Corresponding URL suffix for the model.

        Raises:
            CoolipyAPIServiceException: If the model type is not found in the model_map.
        """
        url_complement = None
        
        for model_type, url in model_map.items():
            if isinstance(model, model_type):
                url_complement = url
                break

        if not url_complement:
            raise CoolipyAPIServiceException(
                f"model argument must be one of: {[i for i in model_map.keys()]}."
            )

        return url_complement

    def _handle_response(
        self,
        response: CoolifyAPIResponse,
        return_type: str,
        model: Optional[
            Union[
                ServerModel,
                ResourceModel,
                DeploymentsModel,
                ProjectsModel,
                PrivateKeysModel,
                EnvironmentsModel,
                TeamModel,
                TeamMemberModel,
            ]
        ] = None,
    ) -> CoolifyAPIResponse:
        """
        Handles the API response and maps the data to the specified model.

        Args:
            response (CoolifyAPIResponse): The raw response object from the HTTP request.
            return_type (str): Specifies the expected return type (e.g., single object or list).
            model (Optional[Union[...]]): The model used to map the response data.

        Returns:
            CoolifyAPIResponse: The response object with data mapped to the specified model or returned as raw.
        """
        status_code = response.status_code
        is_successfull = status_code in (200, 201)

        if is_successfull and return_type is not COOLIFY_RETURN_TYPES.raw:
            if return_type is COOLIFY_RETURN_TYPES.single:
                response.data = model(**response.data).pythonify()
            elif return_type is COOLIFY_RETURN_TYPES.list:
                response.data = [model(**i).pythonify() for i in response.data]

        return response
