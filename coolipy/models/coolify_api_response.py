from dataclasses import dataclass
from typing import Any, Dict, List, Union

from coolipy.models.databases import DatabaseModel
from coolipy.models.deployments import DeploymentsModel
from coolipy.models.environs import EnvironmentsModel
from coolipy.models.private_keys import PrivateKeysModel
from coolipy.models.projects import ProjectsModel
from coolipy.models.resources import ResourceModel
from coolipy.models.servers import ServerModel, ServerSettingsModel
from coolipy.models.teams import TeamMemberModel, TeamModel


@dataclass
class CoolifyAPIResponse:
    """
    Coolify API Response object. Composed by 2 data fields:

    status_code (int): the request response status code.
    data (Union[Coolipy data models]).
    """

    status_code: int
    data: Union[
        DeploymentsModel,
        List[DeploymentsModel],
        EnvironmentsModel,
        List[EnvironmentsModel],
        PrivateKeysModel,
        List[PrivateKeysModel],
        ProjectsModel,
        List[ProjectsModel],
        ResourceModel,
        List[ResourceModel],
        ServerModel,
        List[ServerModel],
        ServerSettingsModel,
        TeamModel,
        List[TeamModel],
        TeamMemberModel,
        List[TeamMemberModel],
        DatabaseModel,
        List[DatabaseModel],
        Dict[str, Any],
        str,
    ]
