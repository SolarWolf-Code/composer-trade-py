"""Cash response models."""

from enum import StrEnum

from pydantic import BaseModel


class TransferConstraints(BaseModel):
    """Transfer constraints for an account."""

    model_config = {"populate_by_name": True}

    cash_withdrawable: float | None = None
    cash_depositable_today: float | None = None
    cash_withdrawable_today: float | None = None
    cash_withdrawable_unallocated: float | None = None


class ACHRelationship(BaseModel):
    """An ACH relationship for a bank account."""

    model_config = {"populate_by_name": True}

    broker_account_id: str
    ach_relationship_id: str
    created_at: str
    updated_at: str
    status: str
    broker: str
    nickname: str | None = None
    bank_account_number_last_4: str | None = None
    bank_account_type: str | None = None
    bank_name: str | None = None
    plaid_account_id: str | None = None
    plaid_institution_id: str | None = None


class ACHRelationshipsResponse(BaseModel):
    """Response from getting ACH relationships."""

    model_config = {"populate_by_name": True}

    stripe_customer_missing: bool
    plaid_link_required: bool
    ach_relationships: list[ACHRelationship] = []


class ACHLimits(BaseModel):
    """ACH transfer limits for an account."""

    model_config = {"populate_by_name": True}

    cash_withdrawable: float | None = None
    cash_depositable_today: float | None = None
    cash_withdrawable_today: float | None = None
    cash_withdrawable_unallocated: float | None = None


class TaxWithholding(BaseModel):
    """Tax withholding information for IRA distributions."""

    model_config = {"populate_by_name": True}

    default_rate: float


class ACHTransfer(BaseModel):
    """An ACH transfer record."""

    model_config = {"populate_by_name": True}

    ach_transfer_id: int
    ach_transfer_uuid: str
    ach_transfer_foreign_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    amount: float
    status: str
    direction: str
    recurring_deposit_uuid: str | None = None
    ach_relationship_uuid: str
    broker_account_uuid: str


class Frequency(StrEnum):
    """Recurring deposit frequency."""

    WEEKLY = "WEEKLY"
    SEMIMONTHLY = "SEMIMONTHLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class RecurringDepositStatus(StrEnum):
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
    next_deposit_date: str | None = None
    created_at: str


class RecurringDepositsResponse(BaseModel):
    """Response from getting recurring deposits."""

    model_config = {"populate_by_name": True}

    recurring_deposits: list[RecurringDeposit] = []


class RecurringDepositMeta(BaseModel):
    """Max recurring deposit info for a frequency."""

    model_config = {"populate_by_name": True}

    amount: float | None = None
    next_deposit_date: str


class RecurringDepositsMeta(BaseModel):
    """Response from getting recurring deposit meta."""

    model_config = {"populate_by_name": True}

    WEEKLY: RecurringDepositMeta | None = None
    SEMIMONTHLY: RecurringDepositMeta | None = None
    MONTHLY: RecurringDepositMeta | None = None
    QUARTERLY: RecurringDepositMeta | None = None


class RecurringDepositProjectionReason(StrEnum):
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

    limit_date: str | None = None
    reason: RecurringDepositProjectionReason
