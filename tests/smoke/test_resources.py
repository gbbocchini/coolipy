"""Smoke tests for read-only list endpoints across resources."""

import pytest

pytestmark = pytest.mark.smoke


def test_list_applications(sync_client):
    assert sync_client.applications.list().status_code == 200


def test_list_databases(sync_client):
    assert sync_client.databases.list().status_code == 200


def test_list_services(sync_client):
    assert sync_client.services.list().status_code == 200


def test_list_deployments(sync_client):
    assert sync_client.deployments.list().status_code == 200


def test_list_s3_storages(sync_client):
    assert sync_client.s3_storages.list().status_code == 200


def test_list_private_keys(sync_client):
    assert sync_client.security.list().status_code == 200
