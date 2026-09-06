"""Base model shared by all coolipy data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CoolipyBaseModel(BaseModel):
    """Base class for every coolipy request and response model.

    Unknown fields are ignored so that responses carrying fields coolipy does
    not model yet still validate.
    """

    model_config = ConfigDict(extra="ignore")
