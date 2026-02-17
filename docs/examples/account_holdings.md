# Fetch current holdings

```python
"""
Fetch current holdings
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

holdings = client.portfolio.get_account_holdings(first_account.account_uuid)

print(f"Account Holdings: {holdings}")
```

**Output:**
```
Account Holdings: [Holding(ticker='TQQQ', quantity=249.605885747, asset_class=<AssetClass.EQUITIES: 'EQUITIES'>, options_details=None)]
```
