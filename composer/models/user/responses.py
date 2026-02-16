"""User response models."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class JWTResponse(BaseModel):
    """Response from getting user JWT."""

    model_config = {"populate_by_name": True}

    token: str


class UserPreferencesOnboarding(BaseModel):
    """Onboarding preferences."""

    model_config = {"populate_by_name": True}

    slides_completed: Optional[bool] = None


class UserPreferencesPortfolioGraph(BaseModel):
    """Portfolio graph preferences."""

    model_config = {"populate_by_name": True}

    hide_total: Optional[bool] = None
    mode: Optional[str] = None
    symphonies: Optional[Dict[str, bool]] = None


class UserPreferencesSymphonyTable(BaseModel):
    """Symphony table preferences."""

    model_config = {"populate_by_name": True}

    views: Optional[Dict[str, bool]] = None


class UserPreferencesBanners(BaseModel):
    """Banner preferences."""

    model_config = {"populate_by_name": True}

    dismissed_recurring_deposits: Optional[bool] = Field(None, alias="dismissed-recurring-deposits")
    dismissed_crypto_forty_nine: Optional[bool] = Field(None, alias="dismissed-crypto-forty-nine")
    dismissed_crypto_2pct_bonus: Optional[bool] = Field(None, alias="dismissed-crypto-2pct-bonus")
    dismissed_symphony_history: Optional[bool] = Field(None, alias="dismissed-symphony-history")
    dismissed_options_level_1: Optional[bool] = Field(None, alias="dismissed-options-level-1")
    dismissed_options_1000_contracts_promo: Optional[bool] = Field(
        None, alias="dismissed-options-1000-contracts-promo"
    )
    dismissed_crypto_deprecation: Optional[bool] = Field(None, alias="dismissed-crypto-deprecation")
    dismissed_direct_trading: Optional[bool] = Field(None, alias="dismissed-direct-trading")
    dismissed_trade_preview: Optional[bool] = Field(None, alias="dismissed-trade-preview")
    dismissed_trade_with_ai: Optional[bool] = Field(None, alias="dismissed-trade-with-ai")
    dismissed_options: Optional[bool] = None
    dismissed_run_now: Optional[bool] = Field(None, alias="dismissed-run-now")


class UserPreferences(BaseModel):
    """User preferences."""

    model_config = {"populate_by_name": True}

    onboarding: Optional[UserPreferencesOnboarding] = None
    portfolio_graph: Optional[UserPreferencesPortfolioGraph] = Field(None, alias="portfolio-graph")
    symphony_table: Optional[UserPreferencesSymphonyTable] = Field(None, alias="symphony-table")
    banners: Optional[UserPreferencesBanners] = None


class UserOnboardingStateAccount(BaseModel):
    """Account onboarding state."""

    model_config = {"populate_by_name": True}

    funding_source: Optional[str] = None


class UserOnboardingState(BaseModel):
    """User onboarding state."""

    model_config = {"populate_by_name": True}

    accounts: Dict[str, UserOnboardingStateAccount] = {}


class UserOnboardingExtraInfo(BaseModel):
    """Extra onboarding info."""

    model_config = {"populate_by_name": True}

    kraken_occupation: Optional[str] = None


class UserProfile(BaseModel):
    """User profile response."""

    model_config = {"populate_by_name": True}

    country: Optional[str] = None
    country_of_tax_residence: Optional[str] = None
    state_of_tax_residence: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    onboarding_medium: Optional[str] = None
    onboarding_source: Optional[str] = None
    user_response: Optional[str] = None
    alpaca_bd_accepted: Optional[bool] = None
    referred_by: Optional[str] = None
    referral_code: Optional[str] = None
    investing_style: Optional[str] = None
    investing_horizon: Optional[str] = None
    dismissed_onboarding_banner: Optional[bool] = None
    dismissed_ira_banner: Optional[bool] = None
    dismissed_ios_banner: Optional[bool] = None
    dismissed_crypto_banner: Optional[bool] = None
    dismissed_ira_and_crypto_banner: Optional[bool] = None
    dismissed_trading_pass_banner: Optional[bool] = None
    seen_getting_started: Optional[bool] = None
    has_saved_symphony: Optional[bool] = None
    has_backtested: Optional[bool] = None
    has_sound_on: Optional[bool] = None
    ungated_create_with_ai_requests: Optional[int] = None
    investor_goals: List[str] = []
    tolt_referral: Optional[str] = None
    preferences: Optional[UserPreferences] = None
    onboarding_state: Optional[UserOnboardingState] = None
    onboarding_extra_info: Optional[UserOnboardingExtraInfo] = None
    onboarding_redirect_path: Optional[str] = None
    ai_tos_accepted: Optional[bool] = None


class AgreementStatusResponse(BaseModel):
    """Response from checking agreement status."""

    model_config = {"populate_by_name": True}

    has_agreed: bool
