# Traded Symbols in the Last 30 Days

This example demonstrates how to fetch a list of unique symbols traded in a specific account over the last 30 days.

```python
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta, UTC
import os

from composer import ComposerClient
from composer.models.reports import ReportType
from dotenv import load_dotenv

load_dotenv()

# Initialize the Composer Client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get the first account
all_accounts = client.accounts.list()
first_account = all_accounts.accounts[0]

# Define the time range (last 30 days)
until = datetime.now(UTC)
since = until - timedelta(days=30)

# Fetch the trade activity report as a CSV
csv_data = client.reports.get(
    first_account.account_uuid,
    since.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    until.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    ReportType.TRADE_ACTIVITY,
)

# Load into a pandas DataFrame and extract unique symbols
df = pd.read_csv(StringIO(csv_data))
unique_symbols = df["Symbol"].unique().tolist()

print(f"Symbols traded in last 30 days: {unique_symbols}")
```
