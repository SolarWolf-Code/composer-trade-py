"""Composer API Client.

This module provides the main client for interacting with the Composer API.
"""

from .http_client import HTTPClient, RetryConfig
from .resources.accounts import Accounts
from .resources.ai_agents import AIAgents
from .resources.auth_management import AuthManagement
from .resources.backtest import Backtest
from .resources.cash import Cash
from .resources.conversation import Conversation
from .resources.deploy import DeployResource
from .resources.dry_run import DryRun
from .resources.market_data import MarketData
from .resources.portfolio import Portfolio
from .resources.public_symphony import PublicSymphony
from .resources.public_user import PublicUser
from .resources.quotes import Quotes
from .resources.reports import Reports
from .resources.search import Search
from .resources.trading import Trading
from .resources.user import User
from .resources.user_symphonies import UserSymphonies
from .resources.user_symphony import UserSymphony
from .resources.watchlist import Watchlist

_DEFAULT_RETRY_CONFIG = RetryConfig()


class ComposerClient:
    """Main client for interacting with the Composer API.

    This client provides access to various Composer API resources including
    backtest, market data, trading, portfolio management, and more.

    Args:
        api_key: The API Key ID
        api_secret: The API Secret Key
        timeout: Request timeout in seconds (default: 30.0)
        retry_config: Configuration for retry behavior (default: 3 retries, 10s for 429, 3s for 5xx)
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        timeout: float = 30.0,
        retry_config: RetryConfig | None = _DEFAULT_RETRY_CONFIG,
    ):
        """
        Initialize the Composer Client.

        Args:
            api_key (str): The API Key ID
            api_secret (str): The API Secret Key
            timeout (float): Request timeout in seconds (default: 30.0)
            retry_config (RetryConfig | None): Configuration for retry behavior.
                Pass None to disable retries (default: RetryConfig())
        """
        self.http_client = HTTPClient(
            api_key, api_secret, timeout=timeout, retry_config=retry_config
        )
        # Separate HTTP clients for backtest API (different base URL)
        # Public client (no auth headers) for public endpoints
        # Authenticated client for endpoints requiring auth
        self.backtest_auth_client = HTTPClient(
            api_key,
            api_secret,
            base_url="https://backtest-api.composer.trade/",
            timeout=timeout,
            retry_config=retry_config,
        )
        # Stagehand API client for portfolio/account endpoints
        self.stagehand_auth_client = HTTPClient(
            api_key,
            api_secret,
            base_url="https://stagehand-api.composer.trade/",
            timeout=timeout,
            retry_config=retry_config,
        )
        # Trading API client for deploy and trading endpoints
        self.trading_auth_client = HTTPClient(
            api_key,
            api_secret,
            base_url="https://trading-api.composer.trade/",
            timeout=timeout,
            retry_config=retry_config,
        )

        # Initialize resources
        self.backtest = Backtest(self.backtest_auth_client)
        # Market data uses stagehand API
        self.market_data = MarketData(self.stagehand_auth_client)
        # Accounts, Portfolio, Cash, User, AI Agents, Conversation, Reports, Auth use stagehand API
        self.accounts = Accounts(self.stagehand_auth_client)
        self.portfolio = Portfolio(self.stagehand_auth_client)
        self.cash = Cash(self.stagehand_auth_client)
        self.user = User(self.stagehand_auth_client)
        self.ai_agents = AIAgents(self.stagehand_auth_client)
        self.conversation = Conversation(self.stagehand_auth_client)
        self.reports = Reports(self.stagehand_auth_client)
        self.auth_management = AuthManagement(self.stagehand_auth_client)
        self.search = Search(self.backtest_auth_client)
        # Quotes uses stagehand API (public endpoint)
        self.quotes = Quotes(self.stagehand_auth_client)

        # Public user endpoints
        self.public_user = PublicUser(self.stagehand_auth_client)

        # New backtest API resources
        # Public endpoints (no auth required)
        self.public_symphony = PublicSymphony(self.backtest_auth_client)
        # Authenticated endpoints
        self.user_symphony = UserSymphony(self.backtest_auth_client)
        self.user_symphonies = UserSymphonies(self.backtest_auth_client)
        self.watchlist = Watchlist(self.backtest_auth_client)
        # Trading API resources (deploy, dry-run, and trading endpoints)
        self.deploy = DeployResource(self.trading_auth_client)
        self.dry_run = DryRun(self.trading_auth_client)
        self.trading = Trading(self.trading_auth_client)
