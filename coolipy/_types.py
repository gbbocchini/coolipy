"""Shared type aliases used across coolipy."""

from __future__ import annotations

from typing import Any, TypeAlias

#: Any JSON-compatible value (dict, list, str, int, float, bool, or ``None``).
JSONValue: TypeAlias = Any

#: A Coolify resource UUID (an opaque string).
UUID: TypeAlias = str
