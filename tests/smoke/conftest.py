"""Shared fixtures for real-world smoke tests.

Smoke tests are skipped unless ``COOLIPY_API_KEY`` and ``COOLIPY_ENDPOINT`` are
set in the environment. No secrets are hardcoded anywhere.
"""

from __future__ import annotations

import os

import pytest

from coolipy import AsyncCoolipy, Coolipy


def _require_env() -> None:
    missing = [v for v in ("COOLIPY_API_KEY", "COOLIPY_ENDPOINT") if not os.environ.get(v)]
    if missing:
        pytest.skip(
            f"Smoke tests require env vars: {', '.join(missing)}. "
            "Skipping (no live Coolify instance configured)."
        )


def _client_kwargs() -> dict[str, object]:
    _require_env()
    return {
        "coolify_api_key": os.environ["COOLIPY_API_KEY"],
        "coolify_endpoint": os.environ["COOLIPY_ENDPOINT"],
        "coolify_port": int(os.environ.get("COOLIPY_PORT", "8000")),
        "http_protocol": os.environ.get("COOLIPY_PROTOCOL", "http"),
        "omit_port": os.environ.get("COOLIPY_OMIT_PORT", "false").lower() == "true",
    }


@pytest.fixture()
def sync_client():
    """A synchronous client bound to the configured Coolify instance."""
    client = Coolipy(**_client_kwargs())
    yield client
    client.close()


@pytest.fixture()
async def async_client():
    """An asynchronous client bound to the configured Coolify instance."""
    client = AsyncCoolipy(**_client_kwargs())
    yield client
    await client.close()
