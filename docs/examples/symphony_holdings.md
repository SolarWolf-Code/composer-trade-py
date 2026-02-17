# Fetch symphony holdings

```python
"""
Fetch symphony holdings
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

all_symphonies = client.portfolio.get_symphony_stats_meta(first_account.account_uuid)
first_symphony = all_symphonies.symphonies[0]

first_symphony_holdings = client.portfolio.get_symphony_holdings(first_account.account_uuid, first_symphony.id)

print(f"Symphony Holdings: {first_symphony_holdings.shares}")
```

**Output:**
```
Symphony Holdings: {'TQQQ': 249.605885747}
```
