import unittest
from unittest.mock import patch, MagicMock
from coolipy import Coolipy

class TestCoolipy(unittest.TestCase):
    def setUp(self):
        self.coolify_api_key = "fake_api_key"
        self.coolify_endpoint = "example.com"
        self.coolify_port = 8000
        self.coolify = Coolipy(
            coolify_api_key=self.coolify_api_key,
            coolify_endpoint=self.coolify_endpoint,
            coolify_port=self.coolify_port,
        )

    @patch("requests.get")
    def test_enable_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"status": "enabled"}'
        mock_get.return_value = mock_response

        response = self.coolify.enable_api()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "enabled"})

    @patch("requests.get")
    def test_disable_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"status": "disabled"}'
        mock_get.return_value = mock_response

        response = self.coolify.disable_api()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "disabled"})

    @patch("requests.get")
    def test_healthcheck(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"OK"}'
        mock_get.return_value = mock_response

        response = self.coolify.healthcheck()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '{"OK"}')

    @patch("requests.get")
    def test_version(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '{"version": "1.0.0"}'
        mock_get.return_value = mock_response

        response = self.coolify.version()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"version": "1.0.0"})
