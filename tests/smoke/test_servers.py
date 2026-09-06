"""Smoke tests for the servers resource.

Creating a server is intentionally not tested (requires a live host + SSH key).
"""

import pytest

from coolipy.models.servers import ServerModel

pytestmark = pytest.mark.smoke


def test_list_servers_sync(sync_client):
    resp = sync_client.servers.list()
    assert resp.status_code == 200
    assert all(isinstance(s, ServerModel) for s in resp.data)


def test_get_server_sync(sync_client):
    listed = sync_client.servers.list()
    assert listed.status_code == 200
    if not listed.data:
        pytest.skip("No servers available on this instance")
    server = listed.data[0]
    got = sync_client.servers.get(server.uuid)
    assert got.status_code == 200
    assert isinstance(got.data, ServerModel)


async def test_list_servers_async(async_client):
    resp = await async_client.servers.list()
    assert resp.status_code == 200
