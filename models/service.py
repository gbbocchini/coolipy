from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union, override
from constants import COOLIFY_SERVICE_TYPES
from models.applications import ServiceApplicationModel
from models.base import CoolipyBaseModel
from models.servers import ServerModel


@dataclass
class ServiceModelCreate(CoolipyBaseModel):
    type: COOLIFY_SERVICE_TYPES
    name: str
    environment_name: str
    project_uuid: str
    server_uuid: str
    destination_uuid: str
    instant_deploy: bool
    destination_uuid: str
    description: Optional[str] = None


@dataclass
class ServiceModel(CoolipyBaseModel):
    id: Optional[str] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    applications: Optional[List[ServiceApplicationModel]] = field(default_factory=list)
    compose_parsing_version: Optional[str] = None
    config_hash: Optional[str] = None
    connect_to_docker_network: Optional[bool] = None
    databases: Optional[List[str]] = field(default_factory=list)
    deleted_at: Optional[Union[str, datetime]] = None
    description: Optional[str] = None
    destination_id: Optional[int] = None
    destination_type: Optional[str] = None
    docker_compose: Optional[str] = None
    docker_compose_raw: Optional[str] = None
    environment_id: Optional[int] = None
    laravel_through_key: Optional[str] = None
    is_container_label_escape_enabled: Optional[bool] = None
    server: Optional[ServerModel] = field(default_factory=dict)
    server_id: Optional[int] = None
    server_status: Optional[bool] = None
    domains: Optional[List[str]] = field(default_factory=list)
    service_type: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None

    @override
    def _adjust_nested(self):
        if isinstance(self.applications, list) and len(self.applications):
            raw_apps = self.applications
            parsed_apps = [ServiceApplicationModel(**i).pythonify() for i in raw_apps]
            self.applications = parsed_apps

        if isinstance(self.server, dict) and self.server:
            raw_server = self.server
            parsed_server = ServerModel(**raw_server).pythonify()
            self.server = parsed_server
