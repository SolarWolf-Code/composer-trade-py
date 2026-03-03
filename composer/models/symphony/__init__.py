"""Symphony models - request and response models for symphony endpoints."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AssetClass(StrEnum):
    """Asset class for a symphony."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class BenchmarkType(StrEnum):
    """Type of benchmark."""

    SYMPHONY = "symphony"
    TICKER = "ticker"


class Benchmark(BaseModel):
    """Benchmark for performance comparison."""

    model_config = {"populate_by_name": True}

    is_checked: bool
    color: str
    id: str
    type: BenchmarkType


class CreateSymphonyRequest(BaseModel):
    """Request to create a new symphony."""

    model_config = {"populate_by_name": True}

    name: str = Field(description="Name of the symphony")
    asset_class: AssetClass = Field(
        default=AssetClass.EQUITIES, description="Asset class for the symphony"
    )
    description: str | None = Field(None, description="Description of the symphony")
    color: str = Field(description="Color for the symphony (hex format, e.g., #FFBB38)")
    hashtag: str = Field(description="Hashtag for the symphony (e.g., #BTD)")
    tags: list[str] | None = Field(None, description="Tags for categorizing the symphony")
    # Symphony trading logic - will be wrapped in {"raw_value": ...} when serialized
    symphony: Any | None = Field(
        None, description="The trading logic (SymphonyDefinition node or dict)"
    )
    benchmarks: list[Benchmark] | None = Field(
        None, description="Benchmarks for performance comparison"
    )
    share_with_everyone: bool | None = Field(
        None, description="Whether to share the symphony publicly"
    )


class CreateSymphonyResponse(BaseModel):
    """Response from creating a symphony."""

    model_config = {"populate_by_name": True}

    symphony_id: str = Field(description="ID of the created symphony")
    version_id: str = Field(description="ID of the initial version")


class CopySymphonyRequest(BaseModel):
    """Request to copy a symphony."""

    model_config = {"populate_by_name": True}

    name: str | None = Field(None, description="Name for the copied symphony")
    color: str | None = Field(None, description="Color for the symphony (hex format)")
    hashtag: str | None = Field(None, description="Hashtag for the symphony")
    benchmarks: list[Benchmark] | None = Field(
        None, description="Benchmarks for performance comparison"
    )
    share_with_everyone: bool | None = Field(
        None, description="Whether to share the symphony publicly"
    )
    is_public: bool | None = Field(None, description="DEPRECATED - use share_with_everyone instead")


class CopySymphonyResponse(BaseModel):
    """Response from copying a symphony."""

    model_config = {"populate_by_name": True}

    symphony_id: str = Field(description="ID of the copied symphony")
    version_id: str = Field(description="ID of the initial version")


class UpdateSymphonyResponse(BaseModel):
    """Response from updating a symphony."""

    model_config = {"populate_by_name": True}

    existing_version_id: str = Field(description="ID of the previous version")
    version_id: str | None = Field(None, description="ID of the new version")


class UpdateSymphonyNodesResponse(BaseModel):
    """Response from updating symphony nodes."""

    model_config = {"populate_by_name": True}

    symphony_id: str = Field(description="ID of the symphony")
    version_id: str = Field(description="ID of the new version")


class SymphonyVersion(BaseModel):
    """A version of a symphony."""

    model_config = {"populate_by_name": True}

    version_id: str = Field(description="ID of the version")
    created_at: str = Field(description="When the version was created (ISO 8601)")


class DefSymphonyRequest(BaseModel):
    """Request to convert defsymphony DSL text to symphony score."""

    model_config = {"populate_by_name": True}

    code: str = Field(description="Defsymphony DSL text to convert")


__all__ = [
    "AssetClass",
    "BenchmarkType",
    "Benchmark",
    "CreateSymphonyRequest",
    "CreateSymphonyResponse",
    "CopySymphonyRequest",
    "CopySymphonyResponse",
    "DefSymphonyRequest",
    "UpdateSymphonyResponse",
    "UpdateSymphonyNodesResponse",
    "SymphonyVersion",
]
