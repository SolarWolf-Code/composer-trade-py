"""User response models."""

from pydantic import BaseModel, Field


class JWTResponse(BaseModel):
    """Response from getting user JWT."""

    model_config = {"populate_by_name": True}

    token: str


class UserPreferencesOnboarding(BaseModel):
    """Onboarding preferences."""

    model_config = {"populate_by_name": True}

    slides_completed: bool | None = None


class UserPreferencesPortfolioGraph(BaseModel):
    """Portfolio graph preferences."""

    model_config = {"populate_by_name": True}

    hide_total: bool | None = None
    mode: str | None = None
    symphonies: dict[str, bool] | None = None


class UserPreferencesSymphonyTable(BaseModel):
    """Symphony table preferences."""

    model_config = {"populate_by_name": True}

    views: dict[str, bool] | None = None


class UserPreferencesBanners(BaseModel):
    """Banner preferences."""

    model_config = {"populate_by_name": True}

    dismissed_recurring_deposits: bool | None = Field(None, alias="dismissed-recurring-deposits")
    dismissed_crypto_forty_nine: bool | None = Field(None, alias="dismissed-crypto-forty-nine")
    dismissed_crypto_2pct_bonus: bool | None = Field(None, alias="dismissed-crypto-2pct-bonus")
    dismissed_symphony_history: bool | None = Field(None, alias="dismissed-symphony-history")
    dismissed_options_level_1: bool | None = Field(None, alias="dismissed-options-level-1")
    dismissed_options_1000_contracts_promo: bool | None = Field(
        None, alias="dismissed-options-1000-contracts-promo"
    )
    dismissed_crypto_deprecation: bool | None = Field(None, alias="dismissed-crypto-deprecation")
    dismissed_direct_trading: bool | None = Field(None, alias="dismissed-direct-trading")
    dismissed_trade_preview: bool | None = Field(None, alias="dismissed-trade-preview")
    dismissed_trade_with_ai: bool | None = Field(None, alias="dismissed-trade-with-ai")
    dismissed_options: bool | None = None
    dismissed_run_now: bool | None = Field(None, alias="dismissed-run-now")


class UserPreferences(BaseModel):
    """User preferences."""

    model_config = {"populate_by_name": True}

    onboarding: UserPreferencesOnboarding | None = None
    portfolio_graph: UserPreferencesPortfolioGraph | None = Field(None, alias="portfolio-graph")
    symphony_table: UserPreferencesSymphonyTable | None = Field(None, alias="symphony-table")
    banners: UserPreferencesBanners | None = None


class UserOnboardingStateAccount(BaseModel):
    """Account onboarding state."""

    model_config = {"populate_by_name": True}

    funding_source: str | None = None


class UserOnboardingState(BaseModel):
    """User onboarding state."""

    model_config = {"populate_by_name": True}

    accounts: dict[str, UserOnboardingStateAccount] = {}


class UserOnboardingExtraInfo(BaseModel):
    """Extra onboarding info."""

    model_config = {"populate_by_name": True}

    kraken_occupation: str | None = None


class UserProfile(BaseModel):
    """User profile response."""

    model_config = {"populate_by_name": True}

    country: str | None = None
    country_of_tax_residence: str | None = None
    state_of_tax_residence: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    onboarding_medium: str | None = None
    onboarding_source: str | None = None
    user_response: str | None = None
    alpaca_bd_accepted: bool | None = None
    referred_by: str | None = None
    referral_code: str | None = None
    investing_style: str | None = None
    investing_horizon: str | None = None
    dismissed_onboarding_banner: bool | None = None
    dismissed_ira_banner: bool | None = None
    dismissed_ios_banner: bool | None = None
    dismissed_crypto_banner: bool | None = None
    dismissed_ira_and_crypto_banner: bool | None = None
    dismissed_trading_pass_banner: bool | None = None
    seen_getting_started: bool | None = None
    has_saved_symphony: bool | None = None
    has_backtested: bool | None = None
    has_sound_on: bool | None = None
    ungated_create_with_ai_requests: int | None = None
    investor_goals: list[str] = []
    tolt_referral: str | None = None
    preferences: UserPreferences | None = None
    onboarding_state: UserOnboardingState | None = None
    onboarding_extra_info: UserOnboardingExtraInfo | None = None
    onboarding_redirect_path: str | None = None
    ai_tos_accepted: bool | None = None


class AgreementStatusResponse(BaseModel):
    """Response from checking agreement status."""

    model_config = {"populate_by_name": True}

    has_agreed: bool
