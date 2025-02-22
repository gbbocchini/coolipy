from coolipy.constants import _COOLIFY_RETURN_TYPES, _URL_MAP
from coolipy.models.coolify_api_response import CoolifyAPIResponse
from coolipy.models.teams import TeamMemberModel, TeamModel
from coolipy.services.coolify_api.base import CoolifyApiBase


class Teams(CoolifyApiBase):
    """
    Handles operations related to teams in the Coolify API.
    """

    def list(self) -> CoolifyAPIResponse:
        """
        Retrieve all teams.

        Returns:
            CoolifyAPIResponse: Response containing a list of teams.
        """
        content = self._http.get(self._base_url)
        return self._handle_response(content, _COOLIFY_RETURN_TYPES.list, TeamModel)

    def get(self, team_id: int) -> CoolifyAPIResponse:
        """
        Retrieve a team by ID.

        Args:
            team_id (int): The ID of the team.

        Returns:
            CoolifyAPIResponse: Response containing the team details.
        """
        content = self._http.get(f"{self._base_url}/{team_id}")
        return self._handle_response(content, _COOLIFY_RETURN_TYPES.single, TeamModel)

    def members(self, team_id: int) -> CoolifyAPIResponse:
        """
        Retrieve members of a team.

        Args:
            team_id (int): The ID of the team.

        Returns:
            CoolifyAPIResponse: Response containing a list of team members.
        """
        content = self._http.get(f"{self._base_url}/{team_id}{_URL_MAP.members}")
        return self._handle_response(
            content, _COOLIFY_RETURN_TYPES.list, TeamMemberModel
        )

    def authenticated_team(self) -> CoolifyAPIResponse:
        """
        Retrieve the authenticated user's team.

        Returns:
            CoolifyAPIResponse: Response containing the authenticated team details.
        """
        content = self._http.get(f"{self._base_url}/current")
        return self._handle_response(content, _COOLIFY_RETURN_TYPES.single, TeamModel)

    def authenticated_team_members(self) -> CoolifyAPIResponse:
        """
        Retrieve members of the authenticated user's team.

        Returns:
            CoolifyAPIResponse: Response containing the list of team members.
        """
        content = self._http.get(
            f"{self._base_url}{_URL_MAP.current}{_URL_MAP.members}"
        )
        return self._handle_response(
            content, _COOLIFY_RETURN_TYPES.list, TeamMemberModel
        )
