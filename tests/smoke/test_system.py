"""Smoke tests for system endpoints."""

import pytest

pytestmark = pytest.mark.smoke


def test_version_sync(sync_client):
    resp = sync_client.version()
    assert resp.status_code == 200
    assert isinstance(resp.data, str)


async def test_version_async(async_client):
    resp = await async_client.version()
    assert resp.status_code == 200
    assert isinstance(resp.data, str)


def test_health_sync(sync_client):
    resp = sync_client.health()
    assert resp.status_code == 200


async def test_health_async(async_client):
    resp = await async_client.health()
    assert resp.status_code == 200
