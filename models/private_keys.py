from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from .base import CoolipyBaseModel


@dataclass
class PrivateKeysModel(CoolipyBaseModel):
    """
    Coolify Private Keys data model.
    """

    description: Optional[str] = None
    name: Optional[str] = None
    private_key: Optional[str] = None
    id: Optional[int] = None
    uuid: Optional[str] = None
    fingerprint: Optional[str] = None
    is_git_related: Optional[bool] = None
    team_id: Optional[int] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None


@dataclass
class PrivateKeysModelCreate:
    description: str
    name: str
    private_key: str
