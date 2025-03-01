from coolipy.models.coolify_api_response import CoolifyAPIResponse
from coolipy.services.coolify_api.applications import Applications
from coolipy.services.coolify_api.deployments import Deployments
from coolipy.services.coolify_api.private_keys import PrivatetKeys
from coolipy.services.coolify_api.projects import Projects
from coolipy.services.coolify_api.resources import Resources
from coolipy.services.coolify_api.servers import Servers
from coolipy.services.coolify_api.services import Services
from coolipy.services.coolify_api.teams import Teams
from coolipy.services.coolify_api.databases import Databases
from coolipy.services.http_service import HttpService
from coolipy.constants import API_BASE_ENTRYPOINT, URL_MAP


class Coolipy:
    """
    The main entry point for interacting with the Coolify API using Coolipy.

    This class provides methods and modules to access various Coolify resources,
    such as projects, deployments, servers, and more. It handles authentication,
    API requests, and resource management for easy integration with the Coolify
    platform.

    Attributes:
        projects (Projects): Manages operations related to projects.
        deployments (Deployments): Handles deployment-related functionalities.
        resources (Resources): Provides access to resource management.
        servers (Servers): Facilitates interactions with server-related endpoints.
        private_keys (PrivateKeys): Manages private keys.
        teams (Teams): Handles team-related operations.
        services (Services): Accesses Coolify services.
        databases (Databases): Interacts with database functionalities.
        applications (Applications): Manages application-related operations.

    Args:
        coolify_api_key (str): The API key for authenticating with the Coolify API.
        coolify_endpoint (str): The endpoint URL of the Coolify server.
        coolify_port (int, optional): The port number for the Coolify server. Defaults to 8000.
        omit_port (bool, optional): Flag for DNS resolution (no port in the Coolify url). Defaults to False.
        http_protocol (str, optional): The HTTP protocol (e.g., "http" or "https"). Defaults to "http".

    Methods:
        enable_api() -> CoolifyAPIResponse:
            Enables the Coolify API.

        disable_api() -> CoolifyAPIResponse:
            Disables the Coolify API.

        healthcheck() -> CoolifyAPIResponse:
            Checks the health status of the Coolify server.

        version() -> CoolifyAPIResponse:
            Retrieves the current version of the Coolify server.
    """

    _slots__ = (
        "coolify_api_key",
        "coolify_endpoint",
        "coolify_port",
        "omit_port",
        "http_protocol",
    )

    def __init__(
        self,
        coolify_api_key: str,
        coolify_endpoint: str,
        coolify_port: int = 8000,
        omit_port: bool = False,
        http_protocol: str = "http",
    ):
        self._coolify_url = (
            f"{http_protocol}://{coolify_endpoint}"
            if omit_port
            else f"{http_protocol}://{coolify_endpoint}:{coolify_port}"
        )
        self._api_base_endpoint = f"{self._coolify_url}{API_BASE_ENTRYPOINT}"
        self._coolify_api_key = coolify_api_key
        self._http = HttpService(
            api_base_endpoint=self._api_base_endpoint,
            bearer_token=self._coolify_api_key,
        )
        self.projects = Projects(
            http_service=self._http, base_service_url=URL_MAP.projects
        )
        self.deployments = Deployments(
            http_service=self._http, base_service_url=URL_MAP.deployments
        )
        self.resources = Resources(
            http_service=self._http, base_service_url=URL_MAP.resources
        )
        self.servers = Servers(
            http_service=self._http, base_service_url=URL_MAP.servers
        )
        self.private_keys = PrivatetKeys(
            http_service=self._http, base_service_url=URL_MAP.private_keys
        )
        self.teams = Teams(http_service=self._http, base_service_url=URL_MAP.teams)
        self.services = Services(
            http_service=self._http, base_service_url=URL_MAP.services
        )
        self.databases = Databases(
            http_service=self._http, base_service_url=URL_MAP.databases
        )
        self.applications = Applications(
            http_service=self._http, base_service_url=URL_MAP.applications
        )

    def enable_api(self) -> CoolifyAPIResponse:
        """
        Enables the Coolify API.

        This method sends a request to enable the Coolify API on the target server.

        Returns:
            CoolifyAPIResponse: The response object containing the status of the operation.
        """
        content = self._http.get(f"{self._coolify_url}{URL_MAP.enable}")
        return content

    def disable_api(self) -> CoolifyAPIResponse:
        """
        Disables the Coolify API.

        This method sends a request to disable the Coolify API on the target server.

        Returns:
            CoolifyAPIResponse: The response object containing the status of the operation.
        """
        content = self._http.get(f"{self._coolify_url}{URL_MAP.disable}")
        return content

    def healthcheck(self) -> CoolifyAPIResponse:
        """
        Performs a health check on the Coolify server.

        This method verifies the server's status and ensures it is operational.

        Returns:
            CoolifyAPIResponse: The response object containing the server's health status.
        """
        content = self._http.get(f"{self._coolify_url}{URL_MAP.health}")
        return content

    def version(self) -> CoolifyAPIResponse:
        """
        Retrieves the current version of the Coolify server.

        This method fetches version details from the server, including the API version.

        Returns:
            CoolifyAPIResponse: The response object containing the server version information.
        """
        content = self._http.get(f"{self._coolify_url}{URL_MAP.version}")
        return content
