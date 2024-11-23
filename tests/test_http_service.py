import unittest
from unittest.mock import patch, MagicMock
from coolipy.services.http_service import HttpService, CoolipyHttpServiceException

class TestHttpService(unittest.TestCase):
    def setUp(self):
        self.api_base_endpoint = "http://example.com/api"
        self.bearer_token = "fake_token"
        self.http_service = HttpService(self.api_base_endpoint, self.bearer_token)

    @patch("requests.get")
    def test_get(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"key": "value"}'
        mock_get.return_value = mock_response

        response = self.http_service.get("/endpoint")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"key": "value"})

    @patch("requests.post")
    def test_post(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = '{"key": "value"}'
        mock_post.return_value = mock_response

        response = self.http_service.post("/endpoint", data={"key": "value"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"key": "value"})

    @patch("requests.patch")
    def test_patch(self, mock_patch):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"key": "updated_value"}'
        mock_patch.return_value = mock_response

        response = self.http_service.patch("/endpoint", data={"key": "updated_value"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"key": "updated_value"})

    @patch("requests.delete")
    def test_delete(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = ""
        mock_delete.return_value = mock_response

        response = self.http_service.delete("/endpoint")
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, "")

    @patch("requests.get")
    def test_make_request_exception(self, mock_get):
        mock_get.side_effect = Exception("Request failed")

        with self.assertRaises(CoolipyHttpServiceException):
            self.http_service._make_request("get", "/endpoint")
