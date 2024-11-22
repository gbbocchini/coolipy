from dataclasses import asdict
import json
from constants import COOLIFY_RETURN_TYPES, URL_MAP
from models.coolify_api_response import CoolifyAPIResponse
from models.resources import ResourceModel
from models.servers import ServerModel, ServerModelCreate
from .base import CoolifyApiBase


class Servers(CoolifyApiBase):
    """
    Handles operations related to servers in the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieve all servers.

        Returns:
            CoolifyAPIResponse: Response containing a list of servers.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.list, model=ServerModel
        )

    def get(self, server_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve a server by UUID.

        Args:
            server_uuid (str): The UUID of the server.

        Returns:
            CoolifyAPIResponse: Response containing the server details.
        """
        content = self._http.get(f"{self._base_url}/{server_uuid}")
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.single, model=ServerModel
        )

    def domains(self, server_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve domains associated with a server.

        Args:
            server_uuid (str): The UUID of the server.

        Returns:
            CoolifyAPIResponse: Response containing the list of domains.
        """
        content = self._http.get(f"{self._base_url}/{server_uuid}{URL_MAP.domains}")
        return self._handle_response(content, return_type=COOLIFY_RETURN_TYPES.raw)

    def resources(self, server_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve resources associated with a server.

        Args:
            server_uuid (str): The UUID of the server.

        Returns:
            CoolifyAPIResponse: Response containing a list of resources.
        """
        content = self._http.get(f"{self._base_url}/{server_uuid}{URL_MAP.resources}")
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.list, model=ResourceModel
        )

    def validate(self, server_uuid: str) -> CoolifyAPIResponse:
        """
        Validate a server configuration.

        Args:
            server_uuid (str): The UUID of the server.

        Returns:
            CoolifyAPIResponse: Response from the validation process.
        """
        content = self._http.get(f"{self._base_url}/{server_uuid}{URL_MAP.validate}")
        return self._handle_response(content, return_type=COOLIFY_RETURN_TYPES.raw)

    def create(
        self,
        server: ServerModelCreate,
    ) -> CoolifyAPIResponse:
        """
        Create a new server.

        Args:
            server (ServerModel): The server data.

        Returns:
            CoolifyAPIResponse: Response containing the created server details.
        """
        server_as_dict = asdict(server)
        resp = self._http.post(self._base_url, data=json.dumps(server_as_dict))
        return self._handle_response(resp, return_type=COOLIFY_RETURN_TYPES.raw)

    def update(
        self,
        updated_server: ServerModelCreate,
    ) -> CoolifyAPIResponse:
        """
        Update an existing server.

        Args:
            updated_server (ServerModel): The updated server data.

        Returns:
            CoolifyAPIResponse: Response containing the updated server details.
        """
        server_as_dict = asdict(updated_server)
        resp = self._http.patch(self._base_url, data=json.dumps(server_as_dict))
        return self._handle_response(
            resp, return_type=COOLIFY_RETURN_TYPES.single, model=ServerModel
        )
