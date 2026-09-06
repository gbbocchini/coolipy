"""Smoke tests for the tags resource."""

import pytest

from coolipy.models.common import Tag, TagCreate

pytestmark = pytest.mark.smoke


def test_tag_lifecycle_sync(sync_client, suffix):
    created = sync_client.tags.create(TagCreate(name=f"coolipy-smoke-tag-{suffix}"))
    assert created.status_code == 201
    assert isinstance(created.data, Tag)
    tag_uuid = created.data.uuid

    try:
        listed = sync_client.tags.list()
        assert listed.status_code == 200
        assert all(isinstance(t, Tag) for t in listed.data)
    finally:
        sync_client.tags.delete(tag_uuid)


async def test_list_tags_async(async_client):
    resp = await async_client.tags.list()
    assert resp.status_code == 200
