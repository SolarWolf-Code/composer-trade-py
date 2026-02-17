# Fetch accounts returns

```python
"""
Fetch accounts returns
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

portfolio_returns = client.portfolio.get_portfolio_history(first_account.account_uuid)

print(f"First 5 Days: {portfolio_returns.series[:5]}")
```

**Output:**
```
First 5 Days: [500.0, 503.11, 529.13, 535.27, 547.76]
```
