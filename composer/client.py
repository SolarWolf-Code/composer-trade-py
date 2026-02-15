from .http_client import HTTPClient
from .resources.accounts import Accounts
from .resources.portfolio import Portfolio
from .resources.symphony import Symphony
from .resources.deploy import Deploy
from .resources.reports import Reports
from .resources.trading import Trading
from .resources.dry_run import DryRun
from .resources.backtest import Backtest
from .resources.market_data import MarketData
from .resources.search import Search


class ComposerClient:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Composer Client.

        Args:
            api_key (str): The API Key ID
            api_secret (str): The API Secret Key
        """
        self.http_client = HTTPClient(api_key, api_secret)

        # Initialize resources
        self.accounts = Accounts(self.http_client)
        self.portfolio = Portfolio(self.http_client)
        self.symphony = Symphony(self.http_client)
        self.deploy = Deploy(self.http_client)
        self.reports = Reports(self.http_client)
        self.trading = Trading(self.http_client)
        self.dry_run = DryRun(self.http_client)
        self.backtest = Backtest(self.http_client)
        self.market_data = MarketData(self.http_client)
        self.search = Search(self.http_client)
