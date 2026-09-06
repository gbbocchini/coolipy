"""Smoke tests for the projects resource (full request + response lifecycle)."""

import pytest

from coolipy.models.projects import (
    EnvironmentCreateModel,
    EnvironmentModel,
    ProjectCreateModel,
    ProjectModel,
    ProjectUpdateModel,
)

pytestmark = pytest.mark.smoke


def test_project_lifecycle_sync(sync_client, suffix):
    created = sync_client.projects.create(
        ProjectCreateModel(name=f"coolipy-smoke-{suffix}", description="smoke test")
    )
    assert created.status_code == 201
    project_uuid = created.data.uuid

    try:
        listed = sync_client.projects.list()
        assert listed.status_code == 200
        assert all(isinstance(p, ProjectModel) for p in listed.data)

        got = sync_client.projects.get(project_uuid)
        assert got.status_code == 200
        assert got.data.uuid == project_uuid

        updated = sync_client.projects.update(
            project_uuid, ProjectUpdateModel(name=f"coolipy-smoke-updated-{suffix}")
        )
        assert updated.status_code == 201
    finally:
        sync_client.projects.delete(project_uuid)


def test_environment_lifecycle_sync(sync_client, suffix):
    created = sync_client.projects.create(ProjectCreateModel(name=f"coolipy-smoke-env-{suffix}"))
    project_uuid = created.data.uuid
    try:
        env = sync_client.projects.create_environment(
            project_uuid, EnvironmentCreateModel(name="staging")
        )
        assert env.status_code == 201

        envs = sync_client.projects.environments(project_uuid)
        assert envs.status_code == 200
        assert all(isinstance(e, EnvironmentModel) for e in envs.data)
    finally:
        sync_client.projects.delete(project_uuid)


async def test_project_lifecycle_async(async_client, suffix):
    created = await async_client.projects.create(
        ProjectCreateModel(name=f"coolipy-smoke-async-{suffix}", description="smoke")
    )
    assert created.status_code == 201
    project_uuid = created.data.uuid
    try:
        listed = await async_client.projects.list()
        assert listed.status_code == 200
    finally:
        await async_client.projects.delete(project_uuid)
