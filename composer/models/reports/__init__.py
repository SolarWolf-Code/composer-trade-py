"""Reports models."""

from enum import Enum


class ReportType(str, Enum):
    """Type of activity report."""

    TRADE_ACTIVITY = "trade-activity"
    NON_TRADE_ACTIVITY = "non-trade-activity"
