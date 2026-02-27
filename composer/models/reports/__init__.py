"""Reports models."""

from enum import StrEnum


class ReportType(StrEnum):
    """Type of activity report."""

    TRADE_ACTIVITY = "trade-activity"
    NON_TRADE_ACTIVITY = "non-trade-activity"
