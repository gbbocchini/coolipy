import json

import httpx

from coolipy._http import SyncTransport
from coolipy.models.projects import ProjectCreateModel
from coolipy.resources.deployments import Deployments
from coolipy.resources.projects import Projects
from coolipy.resources.tags import Tags


def test_create_project_serializes_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/projects"
        assert json.loads(request.content) == {"name": "MyProject"}
        return httpx.Response(201, json={"uuid": "p1"})

    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = Projects(transport).create(ProjectCreateModel(name="MyProject"))
    finally:
        transport.close()

    assert result.data.uuid == "p1"


def test_deploy_builds_query_params():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/deploy"
        assert request.url.params["tag"] == "web"
        assert request.url.params["force"] == "true"
        return httpx.Response(
            200,
            json={
                "deployments": [
                    {"message": "queued", "resource_uuid": "r1", "deployment_uuid": "d1"}
                ]
            },
        )

    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = Deployments(transport).deploy(tag="web", force=True)
    finally:
        transport.close()

    assert result.data.deployments[0].resource_uuid == "r1"


def test_list_tags():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/tags"
        return httpx.Response(200, json=[{"uuid": "t1", "name": "prod"}])

    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    try:
        result = Tags(transport).list()
    finally:
        transport.close()

    assert result.data[0].name == "prod"
