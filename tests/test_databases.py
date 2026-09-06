import json

import httpx

from coolipy._http import SyncTransport
from coolipy.models.databases import DatabaseModel, PostgreSQLModelCreate
from coolipy.resources.databases import Databases


def _dbs(handler):
    transport = SyncTransport(
        "http://localhost:8000", "key", transport=httpx.MockTransport(handler)
    )
    return Databases(transport), transport


def test_create_postgresql_uses_correct_path_and_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/databases/postgresql"
        assert json.loads(request.content) == {"name": "pg", "postgres_db": "mydb"}
        return httpx.Response(200, json={})

    dbs, transport = _dbs(handler)
    try:
        dbs.create(PostgreSQLModelCreate(name="pg", postgres_db="mydb"))
    finally:
        transport.close()


def test_get_database():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/databases/abc"
        return httpx.Response(200, json={"uuid": "abc", "name": "pg"})

    dbs, transport = _dbs(handler)
    try:
        result = dbs.get("abc")
    finally:
        transport.close()

    assert isinstance(result.data, DatabaseModel)
    assert result.data.name == "pg"
