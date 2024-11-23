from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from coolipy.models.base import CoolipyBaseModel


@dataclass
class DeploymentsModel(CoolipyBaseModel):
    """
    Coolify Deployments data model.
    """

    id: Optional[int] = None
    application_id: Optional[str] = None
    deployment_uuid: Optional[str] = None
    pull_request_id: Optional[int] = None
    force_rebuild: Optional[bool] = None
    commit: Optional[str] = None
    status: Optional[str] = None
    is_webhook: Optional[bool] = None
    is_api: Optional[bool] = None
    logs: Optional[str] = None
    current_process_id: Optional[str] = None
    restart_only: Optional[bool] = None
    git_type: Optional[str] = None
    server_id: Optional[int] = None
    application_name: Optional[str] = None
    server_name: Optional[str] = None
    deployment_url: Optional[str] = None
    destination_id: Optional[str] = None
    only_this_server: Optional[bool] = None
    rollback: Optional[bool] = None
    commit_message: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None
