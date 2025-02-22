import unittest
from unittest.mock import MagicMock
from coolipy.constants import _COOLIFY_RETURN_TYPES
from coolipy.exceptions import CoolipyAPIServiceException
from coolipy.services.coolify_api.base import CoolifyApiBase


class TestCoolifyApiBase(unittest.TestCase):
    def setUp(self):
        self.mock_http_service = MagicMock()
        self.base_url = "http://example.com/api"
        self.api_base = CoolifyApiBase(self.mock_http_service, self.base_url)

    def test_init(self):
        self.assertEqual(self.api_base._http, self.mock_http_service)
        self.assertEqual(self.api_base._base_url, self.base_url)

    def test_build_url_params_from_dict(self):
        params = {"key1": "value1", "key2": "value2"}
        result = self.api_base._build_url_params_from_dict(params)
        self.assertEqual(result, "key1=value1&key2=value2")

    def test_build_url_params_from_empty_dict(self):
        result = self.api_base._build_url_params_from_dict({})
        self.assertEqual(result, "")

    def test_infer_url_suffix_from_model_found(self):
        model = MagicMock()
        model_map = {type(model): "suffix"}
        result = self.api_base._infer_url_sufix_from_model(model, model_map)
        self.assertEqual(result, "suffix")

    def test_infer_url_suffix_from_model_not_found(self):
        model = MagicMock()
        model_map = {}
        with self.assertRaises(CoolipyAPIServiceException):
            self.api_base._infer_url_sufix_from_model(model, model_map)

    def test_handle_response_successful_single(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.data = {"key": "value"}

        mock_model = MagicMock()
        mock_model.return_value.pythonify.return_value = {"key": "value"}

        result = self.api_base._handle_response(
            mock_response, _COOLIFY_RETURN_TYPES.single, mock_model
        )
        self.assertEqual(result.data, {"key": "value"})

    def test_handle_response_successful_list(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.data = [{"key": "value"}, {"key2": "value2"}]

        mock_model = MagicMock()
        mock_model.side_effect = lambda **kwargs: MagicMock(pythonify=lambda: kwargs)

        result = self.api_base._handle_response(
            mock_response, _COOLIFY_RETURN_TYPES.list, mock_model
        )
        self.assertEqual(result.data, [{"key": "value"}, {"key2": "value2"}])

    def test_handle_response_raw(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        result = self.api_base._handle_response(
            mock_response, _COOLIFY_RETURN_TYPES.raw
        )
        self.assertEqual(result, mock_response)
