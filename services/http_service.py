import json
import requests
from models.coolify_api_response import CoolifyAPIResponse
from typing import Dict, Optional


class CoolipyHttpServiceException(Exception):
    pass


class HttpService:
    """
    Coolipy Http interface for managing HTTP requests to the Coolify API.
    """

    def __init__(self, api_base_endpoint: str, bearer_token: str):
        """
        Initializes the HttpService with the base API endpoint and bearer token.

        Args:
            api_base_endpoint (str): Base URL for the Coolify API.
            bearer_token (str): Bearer token for API authentication.
        """
        self._headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        self._api_base_endpoint = api_base_endpoint

    def _make_request(
        self, method: str, url: str, data: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Centralizes and executes all HTTP requests.

        Args:
            method (str): HTTP method (e.g., 'get', 'post').
            url (str): Endpoint URL.
            data (Optional[Dict[str, str]]): JSON payload (if applicable).

        Returns:
            requests.Response: The response object returned by the HTTP request.
        """
        full_url = f"{self._api_base_endpoint}{url}"
        try:
            request_func = getattr(requests, method.lower())
            response = request_func(url=full_url, headers=self._headers, data=data)
        except Exception as exc:
            raise CoolipyHttpServiceException(exc) from exc
        return response

    def get(self, url: str) -> str:
        """
        Performs a GET request to the specified URL.

        Args:
            url (str): The URL to GET.

        Returns:
            str: The response content as a JSON object.
        """
        response = self._make_request("get", url)
        return self._response_handler(response)

    def post(self, url: str, data: Optional[Dict[str, str]] = None) -> str:
        """
        Performs a POST request to the specified URL with optional JSON data.

        Args:
            url (str): The URL to POST to.
            data (Optional[Dict[str, str]]): JSON payload to include in the request.

        Returns:
            str: The response content as a JSON object.
        """
        response = self._make_request("post", url, data)
        return self._response_handler(response)

    def patch(self, url, data):
        """
        Performs a PATCH request to the specified URL with JSON data.

        Args:
            url (str): The URL to PATCH.
            data (Dict[str, str]): JSON data to send with the request.

        Returns:
            str: The response content as a JSON object.
        """
        response = self._make_request("patch", url, data)
        return self._response_handler(response)

    def delete(self, url):
        """
        Performs a DELETE request to the specified URL.

        Args:
            url (str): The URL to DELETE.

        Returns:
            str: The response content as a JSON object.
        """
        response = self._make_request("delete", url)
        return self._response_handler(response)

    @staticmethod
    def _response_handler(
        response: requests.Response,
    ) -> CoolifyAPIResponse:
        """
        Handles the response from an HTTP request and parses the content.

        Args:
            response (requests.Response): The response object to handle.

        Returns:
            CoolifyAPIResponse: A parsed CoolifyAPIResponse object.
        """
        status_code = response.status_code
        content = response.content

        try:
            parsed_content = json.loads(content)
        except (json.JSONDecodeError, TypeError, ValueError):
            parsed_content = content

        return CoolifyAPIResponse(status_code=status_code, data=parsed_content)
