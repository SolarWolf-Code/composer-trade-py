from .http_client import HTTPClient
from .resources.backtest import Backtest
from .resources.market_data import MarketData
from .resources.search import Search
from .resources.public_symphony import PublicSymphony
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
        self.backtest_public_client = HTTPClient(base_url="https://backtest-api.composer.trade/")
        # Authenticated client for endpoints requiring auth
        self.backtest_auth_client = HTTPClient(
            api_key, api_secret, base_url="https://backtest-api.composer.trade/"
        )

        # Initialize resources
        self.backtest = Backtest(self.http_client)
        self.market_data = MarketData(self.http_client)
        self.search = Search(self.backtest_public_client)

        # New backtest API resources
        # Public endpoints (no auth required)
        self.public_symphony = PublicSymphony(self.backtest_public_client)
        # Authenticated endpoints
        self.user_symphony = UserSymphony(self.backtest_auth_client)
        self.user_symphonies = UserSymphonies(self.backtest_auth_client)
        self.watchlist = Watchlist(self.backtest_auth_client)
