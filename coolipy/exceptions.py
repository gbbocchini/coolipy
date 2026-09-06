"""Exceptions raised by coolipy."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class CoolipyError(Exception):
    """Base class for every exception raised by coolipy."""


class CoolipyConfigError(CoolipyError):
    """Raised when the client is misconfigured (e.g. missing API key)."""


class CoolipyValidationError(CoolipyError):
    """Raised when a request model fails client-side validation."""


class CoolipyHTTPError(CoolipyError):
    """Raised when the Coolify API responds with a non-2xx status code.

    Attributes:
        status_code: The HTTP status code returned by the API.
        message: The human-readable ``message`` from the error response body.
        errors: Field-level validation errors, populated for ``422`` responses.
        response: The raw parsed response body, when available.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        errors: Mapping[str, Any] | None = None,
        response: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.errors = errors
        self.response = response

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"
