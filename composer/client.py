from .http_client import HTTPClient
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
from .resources.quotes import Quotes
from .resources.reports import Reports
from .resources.search import Search
from .resources.public_symphony import PublicSymphony
from .resources.trading import Trading
from .resources.user import User
from .resources.user_symphony import UserSymphony
from .resources.user_symphonies import UserSymphonies
from .resources.watchlist import Watchlist


class ComposerClient:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Composer Client.

        Args:
            api_key (str): The API Key ID
            api_secret (str): The API Secret Key
        """
        self.http_client = HTTPClient(api_key, api_secret)
        # Separate HTTP clients for backtest API (different base URL)
        # Public client (no auth headers) for public endpoints
        # Authenticated client for endpoints requiring auth
        self.backtest_auth_client = HTTPClient(
            api_key, api_secret, base_url="https://backtest-api.composer.trade/"
        )
        # Stagehand API client for portfolio/account endpoints
        self.stagehand_auth_client = HTTPClient(
            api_key, api_secret, base_url="https://stagehand-api.composer.trade/"
        )
        # Trading API client for deploy and trading endpoints
        self.trading_auth_client = HTTPClient(
            api_key, api_secret, base_url="https://trading-api.composer.trade/"
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
