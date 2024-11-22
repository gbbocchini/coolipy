from constants import COOLIFY_RETURN_TYPES
from models.coolify_api_response import CoolifyAPIResponse
from .base import CoolifyApiBase
from models.resources import ResourceModel


class Resources(CoolifyApiBase):
    """
    Handles operations related to resources in the Coolify API.
    """

    def get(self) -> CoolifyAPIResponse:
        """
        Retrieve all resources.

        Returns:
            CoolifyAPIResponse: Response containing a list of resources.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, return_type=COOLIFY_RETURN_TYPES.list, model=ResourceModel
        )
