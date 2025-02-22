from dataclasses import asdict
import json
from typing import List
from coolipy.constants import _COOLIFY_RETURN_TYPES
from coolipy.models.coolify_api_response import CoolifyAPIResponse
from coolipy.models.private_keys import PrivateKeysModel, PrivateKeysModelCreate
from .base import CoolifyApiBase
from copy import deepcopy


class PrivatetKeys(CoolifyApiBase):
    """
    Handles operations related to private keys in the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieve all private keys.

        Returns:
            CoolifyAPIResponse: Response containing a list of private keys.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(
            content, _COOLIFY_RETURN_TYPES.list, PrivateKeysModel
        )

    def get(self, private_key_uuid: str) -> CoolifyAPIResponse:
        """
        Retrieve a private key by UUID.

        Args:
            private_key_uuid (str): The UUID of the private key.

        Returns:
            CoolifyAPIResponse: Response containing the private key details.
        """
        content = self._http.get(f"{self._base_url}/{private_key_uuid}")
        return self._handle_response(
            content, _COOLIFY_RETURN_TYPES.single, PrivateKeysModel
        )

    def create(self, private_key: PrivateKeysModelCreate) -> CoolifyAPIResponse:
        """
        Create a new private key.

        Args:
            private_key (PrivateKeysModel): The private key data.

        Returns:
            CoolifyAPIResponse: Response from the API.
        """
        model_as_dict = asdict(private_key)
        content = self._http.post(self._base_url, data=json.dumps(model_as_dict))
        return self._handle_response(content, _COOLIFY_RETURN_TYPES.raw)

    def update(self, private_key: PrivateKeysModelCreate) -> CoolifyAPIResponse:
        """
        Update an existing private key.

        Args:
            private_key (PrivateKeysModel): The updated private key data.

        Returns:
            CoolifyAPIResponse: Response from the API.
        """
        model_as_dict = asdict(private_key)
        content = self._http.patch(self._base_url, data=json.dumps(model_as_dict))
        return self._handle_response(content, _COOLIFY_RETURN_TYPES.raw)

    def delete(self, private_key_uuid: str) -> CoolifyAPIResponse:
        """
        Delete a private key by UUID.

        Args:
            private_key_uuid (str): The UUID of the private key.
        """
        content = self._http.delete(f"{self._base_url}/{private_key_uuid}")
        self._handle_response(content, _COOLIFY_RETURN_TYPES.raw)
