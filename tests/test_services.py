import json

import httpx

from coolipy._http import SyncTransport
from coolipy.models.services import ServiceCreateModel, ServiceModel
from coolipy.resources.services import Services


def _svc(handler):
    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    return Services(transport), transport


def test_create_service_serializes_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/services"
        assert json.loads(request.content) == {"name": "svc", "type": "glance"}
        return httpx.Response(201, json={"uuid": "svc-uuid"})

    services, transport = _svc(handler)
    try:
        result = services.create(ServiceCreateModel(name="svc", type="glance"))
    finally:
        transport.close()

    assert result.data["uuid"] == "svc-uuid"


def test_get_service():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/services/abc"
        return httpx.Response(200, json={"uuid": "abc", "name": "svc"})

    services, transport = _svc(handler)
    try:
        result = services.get("abc")
    finally:
        transport.close()

    assert isinstance(result.data, ServiceModel)
