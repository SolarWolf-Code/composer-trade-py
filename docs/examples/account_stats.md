# Fetch accounts stats

```python
"""
Fetch accounts stats
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

all_accounts = client.accounts.list()
first_account = all_accounts.accounts[0]

portfolio_stats = client.portfolio.get_total_stats(first_account.account_uuid)

print(f"First 5 Days: {portfolio_stats}")
```

**Output:**
```
First 5 Days: portfolio_value=12129.657282157 simple_return=-0.07393 time_weighted_return=0.07565241645564758 net_deposits=13098.13 todays_dollar_change=52.417236007 todays_percent_change=0.00434016678 total_cash=31.26 total_unallocated_cash=18.1 pending_withdrawals=0.0 pending_net_deposits=0.0 pending_deploys_cash=0.0
```
