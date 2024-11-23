from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Union, override

from .base import CoolipyBaseModel
from coolipy.models.environs import EnvironmentsModel


@dataclass
class ProjectsModel(CoolipyBaseModel):
    """
    Coolify Projects data model.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None
    uuid: Optional[str] = None
    default_environment: Optional[str] = None
    environments: list[Optional[EnvironmentsModel]] = field(default_factory=list)
    team_id: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None

    @override
    def _adjust_nested(self):
        if isinstance(self.environments, list) and len(self.environments):
            raw_envs = self.environments
            parsed_envs = [EnvironmentsModel(**i).pythonify() for i in raw_envs]
            self.environments = parsed_envs
