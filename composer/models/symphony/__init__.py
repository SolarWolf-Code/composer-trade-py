"""Symphony models - request and response models for symphony endpoints."""

from typing import List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class AssetClass(str, Enum):
    """Asset class for a symphony."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class BenchmarkType(str, Enum):
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
    description: Optional[str] = Field(None, description="Description of the symphony")
    color: str = Field(description="Color for the symphony (hex format, e.g., #FFBB38)")
    hashtag: str = Field(description="Hashtag for the symphony (e.g., #BTD)")
    tags: Optional[List[str]] = Field(None, description="Tags for categorizing the symphony")
    # Symphony trading logic - will be wrapped in {"raw_value": ...} when serialized
    symphony: Optional[Any] = Field(
        None, description="The trading logic (SymphonyDefinition node or dict)"
    )
    benchmarks: Optional[List[Benchmark]] = Field(
        None, description="Benchmarks for performance comparison"
    )
    share_with_everyone: Optional[bool] = Field(
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

    name: Optional[str] = Field(None, description="Name for the copied symphony")
    color: Optional[str] = Field(None, description="Color for the symphony (hex format)")
    hashtag: Optional[str] = Field(None, description="Hashtag for the symphony")
    benchmarks: Optional[List[Benchmark]] = Field(
        None, description="Benchmarks for performance comparison"
    )
    share_with_everyone: Optional[bool] = Field(
        None, description="Whether to share the symphony publicly"
    )
    is_public: Optional[bool] = Field(
        None, description="DEPRECATED - use share_with_everyone instead"
    )


class CopySymphonyResponse(BaseModel):
    """Response from copying a symphony."""

    model_config = {"populate_by_name": True}

    symphony_id: str = Field(description="ID of the copied symphony")
    version_id: str = Field(description="ID of the initial version")


class UpdateSymphonyResponse(BaseModel):
    """Response from updating a symphony."""

    model_config = {"populate_by_name": True}

    existing_version_id: str = Field(description="ID of the previous version")
    version_id: Optional[str] = Field(None, description="ID of the new version")


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


__all__ = [
    "AssetClass",
    "BenchmarkType",
    "Benchmark",
    "CreateSymphonyRequest",
    "CreateSymphonyResponse",
    "CopySymphonyRequest",
    "CopySymphonyResponse",
    "UpdateSymphonyResponse",
    "UpdateSymphonyNodesResponse",
    "SymphonyVersion",
]
