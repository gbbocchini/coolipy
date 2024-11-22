from models.coolify_api_response import CoolifyAPIResponse
from services.coolify_api.applications import Applications
from services.coolify_api.deployments import Deployments
from services.coolify_api.private_keys import PrivatetKeys
from services.coolify_api.projects import Projects
from services.coolify_api.resources import Resources
from services.coolify_api.servers import Servers
from services.coolify_api.services import Services
from services.coolify_api.teams import Teams
from services.coolify_api.databases import Databases
from services.http_service import HttpService
from constants import API_BASE_ENTRYPOINT, URL_MAP


class Coolipy:
    def __init__(
        self,
        coolify_api_key: str,
        coolify_endpoint: str,
        coolify_port: int = 8000,
        http_protocol: str = "http"
    ):
        self._coolify_url = f"{http_protocol}://{coolify_endpoint}:{coolify_port}"
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
        content = self._http.get(f"{self._coolify_url}{URL_MAP.enable}")
        return content

    def disable_api(self) -> CoolifyAPIResponse:
        content = self._http.get(f"{self._coolify_url}{URL_MAP.disable}")
        return content

    def healthcheck(self) -> CoolifyAPIResponse:
        content = self._http.get(f"{self._coolify_url}{URL_MAP.health}")
        return content
    
    def version(self) -> CoolifyAPIResponse:
        content = self._http.get(f"{self._coolify_url}{URL_MAP.version}")
        return content

