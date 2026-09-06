"""Smoke tests for teams and shared environment variables."""

import pytest

from coolipy.models.teams import TeamModel, UserModel

pytestmark = pytest.mark.smoke


def test_list_teams_sync(sync_client):
    resp = sync_client.teams.list()
    assert resp.status_code == 200
    assert all(isinstance(t, TeamModel) for t in resp.data)


def test_current_team_sync(sync_client):
    resp = sync_client.teams.current()
    assert resp.status_code == 200
    assert isinstance(resp.data, TeamModel)


def test_current_members_sync(sync_client):
    resp = sync_client.teams.current_members()
    assert resp.status_code == 200
    assert all(isinstance(u, UserModel) for u in resp.data)


async def test_list_teams_async(async_client):
    resp = await async_client.teams.list()
    assert resp.status_code == 200
