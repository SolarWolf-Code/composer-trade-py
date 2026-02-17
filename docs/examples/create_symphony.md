# Create a new symphony programatically

```python
"""
Create a new symphony programatically
"""

from composer import ComposerClient
from composer.models.common.symphony import Asset, WeightCashEqual, SymphonyDefinition
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Build a simple strategy
symphony = SymphonyDefinition(
    name="Buy and Hold AAPL",
    description="Simple buy and hold strategy",
    rebalance="daily",
    children=[
        WeightCashEqual(
            children=[Asset(ticker="AAPL", name="Apple Inc")]
        )
    ]
)

# Create it in your account
result = client.user_symphony.create_symphony(
    name="Buy and Hold AAPL",
    color="#FF6B6B",
    hashtag="#AAPL",
    symphony=symphony
)
print(f"Created symphony: {result.symphony_id}")
```

**Output:**
```
Created symphony: T3mnMsUdt9KRLIZxHKNX
```
