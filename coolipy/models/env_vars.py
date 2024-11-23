from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from coolipy.models.base import CoolipyBaseModel


@dataclass
class EnvVarModel(CoolipyBaseModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    application_id: Optional[int] = None
    service_id: Optional[int] = None
    database_id: Optional[int] = None
    is_build_time: Optional[bool] = None
    is_literal: Optional[bool] = None
    is_multiline: Optional[bool] = None
    is_preview: Optional[bool] = None
    is_shared: Optional[bool] = None
    is_shown_once: Optional[bool] = None
    is_really_required: Optional[bool] = None
    is_required: Optional[bool] = None
    order: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None
    real_value: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None


@dataclass
class EnvVarModelsCreate:
    key: str
    value: str
    is_preview: bool
    is_build_time: bool
    is_literal: bool
    is_multiline: bool
    is_shown_once: bool
