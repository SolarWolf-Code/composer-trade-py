"""
Symphony Score Schema - Complete type definitions for Composer trading strategies.

This module defines all node types used to build automated trading strategies (Symphonies).
Each symphony is a tree structure with a Root node containing nested weight, filter,
if/else, and asset nodes.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Literal, Any, TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid


class Function(str, Enum):
    """
    Mathematical and technical analysis functions available for conditions and filters.
    """

    CUMULATIVE_RETURN = "cumulative-return"
    CURRENT_PRICE = "current-price"
    EXPONENTIAL_MOVING_AVERAGE_PRICE = "exponential-moving-average-price"
    MAX_DRAWDOWN = "max-drawdown"
    MOVING_AVERAGE_PRICE = "moving-average-price"
    MOVING_AVERAGE_RETURN = "moving-average-return"
    RELATIVE_STRENGTH_INDEX = "relative-strength-index"
    STANDARD_DEVIATION_PRICE = "standard-deviation-price"
    STANDARD_DEVIATION_RETURN = "standard-deviation-return"


class RebalanceFrequency(str, Enum):
    """How often the symphony should rebalance its holdings."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class WeightMap(BaseModel):
    """
    Weight fraction represented as numerator/denominator.

    Examples:
        - 50% = num: 50, den: 100
        - 33.3% = num: 33.3, den: 100
    """

    model_config = {"populate_by_name": True}

    num: Union[str, int, float] = Field(description="Numerator of the weight fraction")
    den: Union[str, int, float] = Field(
        description="Denominator of the weight fraction (typically 100)"
    )

    @field_validator("num", "den")
    @classmethod
    def validate_positive(cls, v):
        """Ensure weight values are positive."""
        val = float(v) if isinstance(v, str) else v
        if val <= 0:
            raise ValueError("Weight numerator and denominator must be positive")
        return v


# Type variable for recursive child types
ChildType = Any


class BaseNode(BaseModel):
    """
    Base class for all symphony nodes.
    """

    model_config = {"populate_by_name": True, "extra": "ignore"}

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this node (auto-generated UUID or custom ID)",
    )
    weight: Optional[WeightMap] = Field(
        None, description="Weight fraction for this node"
    )


class Asset(BaseNode):
    """A ticker/asset node representing a security to trade."""

    model_config = {"populate_by_name": True}

    step: Literal["asset"] = Field(default="asset")
    name: Optional[str] = Field(None, description="Display name of the asset")
    ticker: str = Field(description="Ticker symbol (e.g., AAPL, CRYPTO::BTC//USD)")
    exchange: Optional[str] = Field(None, description="Exchange code (e.g., XNAS)")
    price: Optional[float] = Field(None, description="Current price (API-populated)")
    dollar_volume: Optional[float] = Field(None, alias="dollar_volume")
    has_marketcap: Optional[bool] = Field(None, alias="has_marketcap")
    children_count: Optional[int] = Field(None, alias="children-count")


class Empty(BaseNode):
    """Empty/cash placeholder node."""

    model_config = {"populate_by_name": True}

    step: Literal["empty"] = Field(default="empty")


class IfChildTrue(BaseNode):
    """The 'true' branch of an If condition."""

    model_config = {"populate_by_name": True}

    step: Literal["if-child"] = Field(default="if-child")
    is_else_condition: Literal[False] = Field(False, alias="is-else-condition?")
    comparator: Literal["gt", "gte", "eq", "lt", "lte"] = Field(
        description="Comparison operator"
    )
    lhs_fn: Function = Field(alias="lhs-fn")
    lhs_window_days: Optional[int] = Field(None, alias="lhs-window-days")
    lhs_val: str = Field(alias="lhs-val")
    rhs_val: Union[str, float] = Field(alias="rhs-val")
    rhs_fixed_value: bool = Field(alias="rhs-fixed-value?")
    rhs_fn: Optional[Function] = Field(None, alias="rhs-fn")
    rhs_window_days: Optional[int] = Field(None, alias="rhs-window-days")
    children: List[Any] = Field(default_factory=list)


class IfChildFalse(BaseNode):
    """The 'false' (else) branch of an If condition."""

    model_config = {"populate_by_name": True}

    step: Literal["if-child"] = Field(default="if-child")
    is_else_condition: Literal[True] = Field(True, alias="is-else-condition?")
    children: List[Any] = Field(default_factory=list)


class If(BaseNode):
    """If/Else conditional node."""

    model_config = {"populate_by_name": True}

    step: Literal["if"] = Field(default="if")
    children: List[Union[IfChildTrue, IfChildFalse]] = Field(default_factory=list)

    @field_validator("children")
    @classmethod
    def validate_if_children(cls, v):
        """Ensure If node has exactly one true and one false child."""
        if len(v) != 2:
            raise ValueError("If node must have exactly 2 children")

        true_count = sum(1 for child in v if not child.is_else_condition)
        false_count = sum(1 for child in v if child.is_else_condition)

        if true_count != 1 or false_count != 1:
            raise ValueError("If node must have one true and one false condition")

        return v


class Filter(BaseNode):
    """Filter node for selecting top/bottom N assets."""

    model_config = {"populate_by_name": True}

    step: Literal["filter"] = Field(default="filter")
    select_: Optional[bool] = Field(None, alias="select?")
    select_fn: Optional[Literal["top", "bottom"]] = Field(None, alias="select-fn")
    select_n: Optional[int] = Field(None, alias="select-n")
    sort_by_: Optional[bool] = Field(None, alias="sort-by?")
    sort_by_fn: Optional[Function] = Field(None, alias="sort-by-fn")
    sort_by_window_days: Optional[int] = Field(None, alias="sort-by-window-days")
    children: List[Any] = Field(default_factory=list)


class WeightInverseVol(BaseNode):
    """Inverse volatility weighting."""

    model_config = {"populate_by_name": True}

    step: Literal["wt-inverse-vol"] = Field(default="wt-inverse-vol")
    window_days: Optional[int] = Field(None, alias="window-days")
    children: List[Any] = Field(default_factory=list)


class Group(BaseNode):
    """Group node containing a single weight strategy."""

    model_config = {"populate_by_name": True}

    step: Literal["group"] = Field(default="group")
    name: Optional[str] = Field(None)
    children: List[Any] = Field(default_factory=list)

    @field_validator("children")
    @classmethod
    def validate_single_child(cls, v):
        if len(v) != 1:
            raise ValueError("Group must have exactly one child")
        return v


class WeightCashEqual(BaseNode):
    """Equal weighting across all children."""

    model_config = {"populate_by_name": True}

    step: Literal["wt-cash-equal"] = Field(default="wt-cash-equal")
    children: List[Any] = Field(default_factory=list)


class WeightCashSpecified(BaseNode):
    """Specified weighting with explicit weights."""

    model_config = {"populate_by_name": True}

    step: Literal["wt-cash-specified"] = Field(default="wt-cash-specified")
    children: List[Any] = Field(default_factory=list)


class Root(BaseNode):
    """Root node of a symphony."""

    model_config = {"populate_by_name": True}

    step: Literal["root"] = Field(default="root")
    name: str = Field(description="Display name of the symphony")
    description: str = Field(default="", description="Description of the strategy")
    rebalance: RebalanceFrequency = Field(description="Rebalancing frequency")
    rebalance_corridor_width: Optional[float] = Field(
        None, alias="rebalance-corridor-width"
    )
    children: List[Union[WeightCashEqual, WeightCashSpecified, WeightInverseVol]] = (
        Field(default_factory=list)
    )

    @field_validator("rebalance_corridor_width")
    @classmethod
    def validate_corridor_width(cls, v, info):
        """Corridor width only allowed when rebalance is 'none'."""
        rebalance = info.data.get("rebalance")
        if v is not None and rebalance != "none":
            raise ValueError(
                'rebalance_corridor_width can only be set when rebalance is "none"'
            )
        return v

    @field_validator("children")
    @classmethod
    def validate_single_child(cls, v):
        """Root must have exactly one weight child."""
        if len(v) != 1:
            raise ValueError("Root must have exactly one child")
        return v


# Type alias for convenience
SymphonyScore = Root


def validate_symphony_score(score):
    """
    Validate a symphony score and check crypto rebalancing rules.

    Args:
        score: Symphony score as Root model or dict

    Returns:
        Validated Root model
    """
    if isinstance(score, dict):
        score = Root.model_validate(score)

    # Check for crypto assets
    crypto_tickers = []

    def find_crypto(node):
        """Recursively find crypto assets."""
        if (
            isinstance(node, Asset)
            and node.ticker
            and node.ticker.startswith("CRYPTO::")
        ):
            crypto_tickers.append(node.ticker)
        # Check children recursively for nodes that have children
        elif (
            not isinstance(node, Asset) and hasattr(node, "children") and node.children
        ):
            for child in node.children:
                if isinstance(child, BaseModel):
                    find_crypto(child)

    if score.children:
        find_crypto(score.children[0])

    # Validate crypto rebalancing
    if crypto_tickers and score.rebalance not in ["none", "daily"]:
        raise ValueError(
            f"Symphonies with crypto must use daily or threshold rebalancing. "
            f"Found rebalance={score.rebalance}"
        )

    return score
