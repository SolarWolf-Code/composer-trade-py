"""Accounts models - request and response models for accounts endpoints."""

from typing import List
from pydantic import BaseModel, Field
from .responses import (
    AssetClass,
    DirectTradableAssetClasses,
    Account,
    OptionsDetails,
    Holding,
    InvestorDocument,
    InvestorDocumentCategory,
    AccountsListResponse,
    AccountType,
    AvailableAccountType,
    SupportedRegionsResponse,
    SupportedRegionStates,
    FootprintPlaybook,
    Trade,
    TradeVolumeResponse,
    TradeHistoryItem,
    Identity,
    Address,
    Contact,
    IncomeRange,
    InvestorProfile,
    TrustedContact,
    AccountInfo,
    BuyingPower,
)


class ApiKey(BaseModel):
    """API key information."""

    id: str = Field(description="API key ID")


class ApiKeyWithSecret(BaseModel):
    """API key with secret (only returned on creation)."""

    id: str = Field(description="API key ID")
    secret: str = Field(description="API key secret")


class ApiKeysResponse(BaseModel):
    """Response containing list of API keys."""

    api_keys: List[ApiKey] = Field(description="List of API keys")


class CreateApiKeyResponse(BaseModel):
    """Response from creating an API key."""

    api_key: ApiKeyWithSecret = Field(description="Created API key")


__all__ = [
    "AssetClass",
    "DirectTradableAssetClasses",
    "Account",
    "OptionsDetails",
    "Holding",
    "InvestorDocument",
    "InvestorDocumentCategory",
    "AccountsListResponse",
    "AccountType",
    "AvailableAccountType",
    "SupportedRegionsResponse",
    "SupportedRegionStates",
    "FootprintPlaybook",
    "Trade",
    "TradeVolumeResponse",
    "TradeHistoryItem",
    "Identity",
    "Address",
    "Contact",
    "IncomeRange",
    "InvestorProfile",
    "TrustedContact",
    "AccountInfo",
    "BuyingPower",
    "ApiKey",
    "ApiKeysResponse",
    "CreateApiKeyResponse",
    "ApiKeyWithSecret",
]
