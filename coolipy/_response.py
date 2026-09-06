"""The response envelope returned by every coolipy method."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CoolipyAPIResponse(Generic[T]):
    """A parsed Coolify API response.

    Attributes:
        status_code: The HTTP status code returned by the API.
        data: The parsed (and, when a model is provided, validated) response body.
        headers: The response headers as a plain string mapping.
    """

    status_code: int
    data: T
    headers: dict[str, str] = field(default_factory=dict)
