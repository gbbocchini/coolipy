"""Models for the system-level Coolify endpoints."""

from __future__ import annotations

from coolipy.models.base import CoolipyBaseModel


class SystemMessage(CoolipyBaseModel):
    """A message returned by system endpoints (e.g. enable/disable API, MCP)."""

    message: str
