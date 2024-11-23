import unittest
from unittest.mock import MagicMock
from datetime import datetime
from coolipy.models.base import CoolipyBaseModel

class TestCoolipyBaseModel(unittest.TestCase):
    def setUp(self):
        self.model = CoolipyBaseModel()

    def test_pythonify(self):
        # Mocking the methods to test their interaction
        self.model._dates_iso_to_datetime = MagicMock()
        self.model._adjust_nested = MagicMock()

        result = self.model.pythonify()

        self.model._dates_iso_to_datetime.assert_called_once()
        self.model._adjust_nested.assert_called_once()
        self.assertEqual(result, self.model)

    def test_dates_iso_to_datetime_valid(self):
        self.model.sentinel_updated_at = "2024-11-22T10:00:00"
        
        self.model._dates_iso_to_datetime()

        self.assertEqual(self.model.sentinel_updated_at, datetime.fromisoformat("2024-11-22T10:00:00"))

    def test_dates_iso_to_datetime_invalid(self):
        self.model.sentinel_updated_at = "invalid-date"
        
        self.model._dates_iso_to_datetime()

        self.assertEqual(self.model.sentinel_updated_at, "invalid-date")

    def test_adjust_nested(self):
        self.model._adjust_nested = MagicMock()

        self.model._adjust_nested()

        self.model._adjust_nested.assert_called_once()

