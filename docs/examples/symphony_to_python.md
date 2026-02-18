# Convert Symphony to Python

Convert a Composer symphony to a typed Python definition file that can be used for backtesting.

```python
"""
Convert a symphony to Python definition
"""

from composer import ComposerClient
from composer.utils import symphony_to_python
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get a symphony score
symphony_id = "QNk0uez4kO7gHz8M3bMi"
score = client.public_symphony.get_score(symphony_id)

# Convert to Python - writes to {symphony_id}.py
symphony_to_python(score)

# Or with options
symphony_to_python(
    score,
    output="my_symphony.py",  # custom output file
    dedup=True,                 # enable deduplication of repeated Groups
    min_hits=2,                # threshold for deduplication
)
```

## Output

The generated Python file looks like:

```python
"""Symphony definition for QNk0uez4kO7gHz8M3bMi"""

from composer.models.common.symphony import *
from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

symph = SymphonyDefinition(
    id="...",
    step="root",
    name="New Symphony",
    description="",
    rebalance=RebalanceFrequency.DAILY,
    children=[
        WeightCashEqual(
            id="...",
            step="wt-cash-equal",
            children=[
                Group(
                    id="...",
                    weight=WeightMap(
                        num=100,
                        den=100,
                    ),
                    step="group",
                    name="Test",
                    collapsed=False,
                    children=[
                        WeightCashEqual(
                            id="...",
                            step="wt-cash-equal",
                            children=[
                                Asset(
                                    id="...",
                                    step="asset",
                                    name="SPDR Gold Shares",
                                    ticker="GLD",
                                    exchange="ARCX",
                                ),
                                # ... more assets
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Backtest
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

res = client.backtest.run_v2(symphony=symph)
print(res)
```

## With Deduplication

When `dedup=True`, repeated Groups are extracted to variables:

```python
symphony_to_python(score, dedup=True)
```

This produces:

```python
# Deduplicated components
group_test_7addb4c6 = Group(
    id="...",
    weight=WeightMap(num=100, den=100),
    step="group",
    name="Test",
    collapsed=False,
    children=[
        WeightCashEqual(...),
    ],
)

symph = SymphonyDefinition(
    ...
    children=[
        WeightCashEqual(
            children=[
                group_test_7addb4c6,  # Reference instead of inline
                group_test_7addb4c6,  # Same group used twice
            ],
        ),
    ],
)
```

The variable name format is `{type}_{sanitized_name}_{hash}`, e.g., `group_test_7addb4c6`.
