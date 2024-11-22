from copy import deepcopy
from datetime import datetime


class CoolipyBaseModel:
    """
    Base data model for Coolipy.
    """

    def pythonify(self) -> "CoolipyBaseModel":
        """
        Transforms the model data, including date conversion and nested processing.

        Calls _dates_iso_to_datetime and _adjust_nested.

        Returns:
            CoolipyBaseModel: The transformed model instance.
        """
        self._dates_iso_to_datetime()
        self._adjust_nested()
        return self

    def _adjust_nested(self):
        """
        Processes any nested models. Use @override!
        """
        pass

    def _dates_iso_to_datetime(self):
        """
        Converts ISO8601 string dates to datetime.datetime objects.
        """
        date_attribs = [
            "sentinel_updated_at",
            "email_verified_at",
            "two_factor_confirmed_at",
            "started_at",
            "stopped_at",
            "created_at",
            "updated_at",
            "deleted_at",
            "last_online_at",
        ]

        for attrib in date_attribs:
            if hasattr(self, attrib):
                try:
                    attrib_copy = deepcopy(getattr(self, attrib))
                    setattr(self, attrib, datetime.fromisoformat(attrib_copy))
                except (ValueError, TypeError, AttributeError):
                    continue
