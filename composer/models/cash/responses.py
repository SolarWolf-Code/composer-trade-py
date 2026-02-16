"""Cash response models."""

from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field


class TransferConstraints(BaseModel):
    """Transfer constraints for an account."""

    model_config = {"populate_by_name": True}

    cash_withdrawable: Optional[float] = None
    cash_depositable_today: Optional[float] = None
    cash_withdrawable_today: Optional[float] = None
    cash_withdrawable_unallocated: Optional[float] = None


class ACHRelationship(BaseModel):
    """An ACH relationship for a bank account."""

    model_config = {"populate_by_name": True}

    broker_account_id: str
    ach_relationship_id: str
    created_at: str
    updated_at: str
    status: str
    broker: str
    nickname: Optional[str] = None
    bank_account_number_last_4: Optional[str] = None
    bank_account_type: Optional[str] = None
    bank_name: Optional[str] = None
    plaid_account_id: Optional[str] = None
    plaid_institution_id: Optional[str] = None


class ACHRelationshipsResponse(BaseModel):
    """Response from getting ACH relationships."""

    model_config = {"populate_by_name": True}

    stripe_customer_missing: bool
    plaid_link_required: bool
    ach_relationships: List[ACHRelationship] = []


class ACHLimits(BaseModel):
    """ACH transfer limits for an account."""

    model_config = {"populate_by_name": True}

    cash_withdrawable: Optional[float] = None
    cash_depositable_today: Optional[float] = None
    cash_withdrawable_today: Optional[float] = None
    cash_withdrawable_unallocated: Optional[float] = None


class TaxWithholding(BaseModel):
    """Tax withholding information for IRA distributions."""

    model_config = {"populate_by_name": True}

    default_rate: float


class ACHTransfer(BaseModel):
    """An ACH transfer record."""

    model_config = {"populate_by_name": True}

    ach_transfer_id: int
    ach_transfer_uuid: str
    ach_transfer_foreign_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    amount: float
    status: str
    direction: str
    recurring_deposit_uuid: Optional[str] = None
    ach_relationship_uuid: str
    broker_account_uuid: str


class Frequency(str, Enum):
    """Recurring deposit frequency."""

    WEEKLY = "WEEKLY"
    SEMIMONTHLY = "SEMIMONTHLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class RecurringDepositStatus(str, Enum):
    """Recurring deposit status."""

    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    PAUSED_BY_COMPOSER = "PAUSED_BY_COMPOSER"
    QUEUED = "QUEUED"


class RecurringDeposit(BaseModel):
    """A recurring deposit."""

    model_config = {"populate_by_name": True}

    recurring_deposit_uuid: str
    broker_account_uuid: str
    amount: float
    frequency: Frequency
    status: RecurringDepositStatus
    next_deposit_date: Optional[str] = None
    created_at: str


class RecurringDepositsResponse(BaseModel):
    """Response from getting recurring deposits."""

    model_config = {"populate_by_name": True}

    recurring_deposits: List[RecurringDeposit] = []


class RecurringDepositMeta(BaseModel):
    """Max recurring deposit info for a frequency."""

    model_config = {"populate_by_name": True}

    amount: Optional[float] = None
    next_deposit_date: str


class RecurringDepositsMeta(BaseModel):
    """Response from getting recurring deposit meta."""

    model_config = {"populate_by_name": True}

    WEEKLY: Optional[RecurringDepositMeta] = None
    SEMIMONTHLY: Optional[RecurringDepositMeta] = None
    MONTHLY: Optional[RecurringDepositMeta] = None
    QUARTERLY: Optional[RecurringDepositMeta] = None


class RecurringDepositProjectionReason(str, Enum):
    """Reason for contribution limit projection."""

    NOT_RETIREMENT_ACCOUNT = "not-retirement-account"
    LIMIT_ALREADY_HIT = "limit-already-hit"
    WONT_HIT_LIMIT = "wont-hit-limit"
    HIT_BEFORE_FIRST_DEPOSIT = "hit-before-first-deposit"
    HIT_OFF_SCHEDULE = "hit-off-schedule"
    HIT_ON_SCHEDULE = "hit-on-schedule"


class RecurringDepositProjection(BaseModel):
    """Projection for when retirement account hits contribution limit."""

    model_config = {"populate_by_name": True}

    limit_date: Optional[str] = None
    reason: RecurringDepositProjectionReason
