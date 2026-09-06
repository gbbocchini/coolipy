"""Coolipy — an (un)official Python client for the Coolify API.

Provides a synchronous client (:class:`Coolipy`) and an asynchronous client
(:class:`AsyncCoolipy`) backed by a single dependency-injected HTTP transport.
"""

from __future__ import annotations

from coolipy._response import CoolipyAPIResponse
from coolipy.async_client import AsyncCoolipy
from coolipy.client import Coolipy
from coolipy.exceptions import (
    CoolipyConfigError,
    CoolipyError,
    CoolipyHTTPError,
    CoolipyValidationError,
)
from coolipy.models.base import CoolipyBaseModel

__version__ = "1.0.0"

__all__ = [
    "AsyncCoolipy",
    "Coolipy",
    "CoolipyAPIResponse",
    "CoolipyBaseModel",
    "CoolipyConfigError",
    "CoolipyError",
    "CoolipyHTTPError",
    "CoolipyValidationError",
    "__version__",
]
