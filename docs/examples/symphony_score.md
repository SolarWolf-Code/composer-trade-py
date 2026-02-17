# Get a symphony score

```python
"""
Get a symphony score
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

# Holy Grail
symphony_id = "QNk0uez4kO7gHz8M3bMi"

score = client.user_symphony.get_score(symphony_id)
print(score)
```

**Output:**
```
id='QNk0uez4kO7gHz8M3bMi' weight=None step='root' name='New Symphony' description='' rebalance=<RebalanceFrequency.DAILY: 'daily'> rebalance_corridor_width=None children=[WeightCashEqual(id='75a1ef11-786f-4185-aad5-cd795982021b', weight=None, step='wt-cash-equal', children=[Group(id='bc9d1750-bbc5-4662-a9cf-5c589077fb15', weight=WeightMap(num=100, den=100), step='group', name='Test', children=[WeightCashEqual(id='b1c5b37d-ec74-4288-8bc3-f42787886d8f', weight=None, step='wt-cash-equal', children=[Asset(id='0c0e7dac-6cd4-4554-9885-844d689fdd41', weight=None, step='asset', name='SSgA Active Trust - State Street SPDR S&P 500 ETF Trust', ticker='SPY', exchange='ARCX', price=None, dollar_volume=None, has_marketcap=None, children_count=None), Asset(id='df234bd0-03a4-429a-a8bb-5925c0a2c109', weight=None, step='asset', name='Invesco Capital Management LLC - Invesco QQQ Trust Series 1', ticker='QQQ', exchange='XNAS', price=None, dollar_volume=None, has_marketcap=None, children_count=None), Asset(id='2ca6cd14-133b-4d23-963a-7a5afaf9f6fa', weight=None, step='asset', name='NVIDIA Corp', ticker='NVDA', exchange='XNAS', price=None, dollar_volume=None, has_marketcap=None, children_count=None)])]), Group(id='22a42dcf-b3e5-4b66-b73b-3c706cf5ee5d', weight=WeightMap(num=100, den=100), step='group', name='Test', children=[WeightCashEqual(id='9d2a046a-e900-4053-a814-2b04285d4a93', weight=None, step='wt-cash-equal', children=[Asset(id='47c28a63-cd3b-44c4-9e07-0a3644727f33', weight=None, step='asset', name='SSgA Active Trust - State Street SPDR S&P 500 ETF Trust', ticker='SPY', exchange='ARCX', price=None, dollar_volume=None, has_marketcap=None, children_count=None), Asset(id='201ea8b8-0083-4662-86a5-d7b5bf279ecd', weight=None, step='asset', name='Invesco Capital Management LLC - Invesco QQQ Trust Series 1', ticker='QQQ', exchange='XNAS', price=None, dollar_volume=None, has_marketcap=None, children_count=None), Asset(id='5da2db4e-afb3-4798-a785-2477c687a844', weight=None, step='asset', name='NVIDIA Corp', ticker='NVDA', exchange='XNAS', price=None, dollar_volume=None, has_marketcap=None, children_count=None)])])])]
```
