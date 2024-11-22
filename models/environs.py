from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Union

from models.base import CoolipyBaseModel
from models.service import ServiceModel


@dataclass
class EnvironmentsModel(CoolipyBaseModel):
    """
    Coolify Environments data model.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    project_id: Optional[int] = None
    created_at: Union[str, datetime] = None
    updated_at: Union[str, datetime] = None
    description: Optional[str] = None
    applications: Optional[str] = None
    mariadbs: list[Any] = field(default_factory=list)
    mongodbs: list[Any] = field(default_factory=list)
    mysqls: list[Any] = field(default_factory=list)
    postgresqls: list[Any] = field(default_factory=list)
    redis: list[Any] = field(default_factory=list)
    services: list[ServiceModel] = field(default_factory=list)

    def _adjust_nested(self):
        if isinstance(self.services, list) and self.services:
            raw_servs = self.services
            parsed = [ServiceModel(**i).pythonify() for i in raw_servs]
            self.services = parsed