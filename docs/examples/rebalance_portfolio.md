# Rebalance Portfolio Based On Weights

```python
"""
Rebalance portfolio based on predefined weights.
"""

import os
from dotenv import load_dotenv
import math

load_dotenv()

from composer import ComposerClient

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

all_accounts = client.accounts.list()
first_account_id = all_accounts.accounts[0].account_uuid

symphony_weights = {
    "VPVpD1SoqR5ykVu4NdWS": 0.50,
    "MCj4VbY9mWWn5LiZVqx8": 0.30,
    "AbyvpflKdp1GLQA7GeIj": 0.20,
}

confirm = input(f"Liquidate all symphonies in account {first_account_id}? (y/n): ")
if confirm.lower() != 'y':
    exit()

# liquidate all symphonies in account
currently_run_symphonies = client.portfolio.get_symphony_stats(first_account_id).stats
for symph in currently_run_symphonies:
    print(f"Liquidating {symph}")
    client.deploy.liquidate(first_account_id, symph)

# wait for cash to settle
import time
time.sleep(10)

account_value = client.portfolio.get_total_stats(first_account_id).portfolio_value

# copy any symphonies you don't own
user_symphs = client.user_symphonies.list_symphonies()
owned_ids = {s.id for s in user_symphs}
not_owned = [s_id for s_id in symphony_weights if s_id not in owned_ids]

for symph_id in not_owned:
    result = client.user_symphony.copy_symphony(symph_id)
    print(f"{symph_id} not owned. Created a copy with new id of: {result.symphony_id}")
    symphony_weights[result.symphony_id] = symphony_weights.pop(symph_id)

# invest based on weights
for symph_id in symphony_weights:
    amount = math.floor(symphony_weights[symph_id] * account_value)
    try:
        client.deploy.invest(first_account_id, symph_id, amount)
        print(f"Invested ${amount} in {symph_id}")
    except:
        print(f"Failed to invest in {symph_id}")
```
