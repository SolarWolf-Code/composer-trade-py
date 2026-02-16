"""Portfolio request models."""

from typing import Optional
from pydantic import BaseModel, Field


class GetAccountHoldingsParams(BaseModel):
    """Query parameters for getting account holdings."""

    model_config = {"populate_by_name": True}

    position_type: Optional[str] = Field(
        None,
        description="Filter by position type: 'direct' for user trades, 'symphony' for Symphony-managed positions",
    )


class GetActivityHistoryParams(BaseModel):
    """Query parameters for getting symphony activity history."""

    model_config = {"populate_by_name": True}

    end_date: Optional[str] = Field(
        None, description="End date for filtering activity (ISO format)"
    )
    start_date: Optional[str] = Field(
        None, description="Start date for filtering activity (ISO format)"
    )
    limit: int = Field(..., description="Maximum number of results to return")
    offset: int = Field(..., description="Offset for pagination")
