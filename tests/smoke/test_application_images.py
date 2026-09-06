"""Smoke tests for creating applications from ready-to-go Docker images.

Resources are left on the instance on purpose — the test instance is disposable
and application deletion is asynchronous in Coolify.
"""

import pytest

from coolipy.models.applications import ApplicationDockerImageModelCreate, ApplicationModel
from coolipy.models.projects import ProjectCreateModel

pytestmark = pytest.mark.smoke

# (image, exposed port) — busybox has no long-running service so no port is exposed.
IMAGES = [
    ("nginx", "80"),
    ("httpd", "80"),
    ("redis", "6379"),
    ("busybox", None),
]


def test_docker_image_application_lifecycle_sync(sync_client, suffix):
    project = sync_client.projects.create(ProjectCreateModel(name=f"coolipy-apps-{suffix}"))
    project_uuid = project.data.uuid

    servers = sync_client.servers.list()
    assert servers.status_code == 200
    server_uuid = servers.data[0].uuid

    for image, port in IMAGES:
        model = ApplicationDockerImageModelCreate(
            project_uuid=project_uuid,
            server_uuid=server_uuid,
            environment_name="production",
            docker_registry_image_name=image,
            docker_registry_image_tag="latest",
            name=f"coolipy-{image}-{suffix}",
            ports_exposes=port,
        )
        created = sync_client.applications.create(model)
        assert created.status_code in (200, 201)
        app_uuid = created.data.uuid

        got = sync_client.applications.get(app_uuid)
        assert got.status_code == 200
        assert isinstance(got.data, ApplicationModel)
        assert got.data.docker_registry_image_name == image

    listed = sync_client.applications.list()
    assert listed.status_code == 200
    assert any(a.docker_registry_image_name == "nginx" for a in listed.data)


async def test_docker_image_application_create_async(async_client, suffix):
    project = await async_client.projects.create(
        ProjectCreateModel(name=f"coolipy-apps-async-{suffix}")
    )
    project_uuid = project.data.uuid

    servers = await async_client.servers.list()
    server_uuid = servers.data[0].uuid

    model = ApplicationDockerImageModelCreate(
        project_uuid=project_uuid,
        server_uuid=server_uuid,
        environment_name="production",
        docker_registry_image_name="nginx",
        docker_registry_image_tag="latest",
        name=f"coolipy-nginx-async-{suffix}",
        ports_exposes="80",
    )
    created = await async_client.applications.create(model)
    assert created.status_code in (200, 201)
    app_uuid = created.data.uuid

    got = await async_client.applications.get(app_uuid)
    assert got.status_code == 200
    assert isinstance(got.data, ApplicationModel)
