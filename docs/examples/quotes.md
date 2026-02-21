# Get Current Quotes

```python
"""
Get current quotes for multiple tickers and convert to DataFrame.
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

quotes = client.quotes.get_quotes(["AAPL", "MSFT", "QQQ"])

print("=== Quotes ===")
print(quotes)
print()

print("=== Quotes DataFrame ===")
print(quotes.df)
```

**Output:**
```
=== Quotes ===
{'EQUITIES::MSFT//USD': QuoteResult(name='Microsoft Corp', price=397.23, previous_price=397.23), 'EQUITIES::AAPL//USD': QuoteResult(name='Apple Inc.', price=264.58, previous_price=264.58), 'EQUITIES::QQQ//USD': QuoteResult(name='Invesco QQQ Trust, Series 1', price=608.81, previous_price=608.81)}

=== Quotes DataFrame ===
                                            name   price  previous_price
ticker                                                                  
EQUITIES::MSFT//USD               Microsoft Corp  397.23          397.23
EQUITIES::AAPL//USD                   Apple Inc.  264.58          264.58
EQUITIES::QQQ//USD   Invesco QQQ Trust, Series 1  608.81          608.81
```
