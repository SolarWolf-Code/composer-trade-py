# Preview rebalance trades for a symphony before actually executing.

```python
"""
Preview rebalance trades for a symphony before actually executing.
This helps you understand what trades will be made without placing them.
"""

from composer import ComposerClient
from composer.http_client import ComposerAPIError
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get first account and symphony (same logic as symphony_holdings example)
all_accounts = client.accounts.list()
first_account = all_accounts.accounts[0]

all_symphonies = client.portfolio.get_symphony_stats_meta(first_account.account_uuid)
first_symphony = all_symphonies.symphonies[0]

symphony_id = first_symphony.id
symphony_name = first_symphony.name or symphony_id

print(f"Previewing rebalance for: {symphony_name}")
print(f"Symphony ID: {symphony_id}")

# Get trade preview with error handling
try:
    preview = client.dry_run.create_trade_preview(
        symphony_id,
        broker_account_uuid=first_account.account_uuid
    )
    
    print("="*60)
    print("REBALANCE PREVIEW SUMMARY")
    print("="*60)

    print(f"Symphony Name: {preview.symphony_name}")
    print(f"Current Value: ${preview.symphony_value:,.2f}")
    print(f"Needs Rebalance: {'Yes' if preview.rebalanced else 'No'}")
    print(f"Next Rebalance After: {preview.next_rebalance_after}")
    print(f"Queued Cash Change: ${preview.queued_cash_change:,.2f}")

    if preview.rebalanced:
        print("\n" + "-"*60)
        print("RECOMMENDED TRADES")
        print("-"*60)
        
        # Display trades in a table format
        print(f"\n{'Symbol':<10} {'Name':<25} {'Side':<6} {'Shares':>10} {'Price':>12} {'Value Chg':>14}")
        print("-"*80)
        
        total_buy = 0
        total_sell = 0
        
        for trade in preview.recommended_trades:
            symbol = trade.symbol
            name = (trade.name[:22] + "...") if trade.name and len(trade.name) > 25 else (trade.name or "")
            side = trade.side.value
            shares = trade.share_change
            price = trade.average_price
            value = trade.cash_change
            
            print(f"{symbol:<10} {name:<25} {side:<6} {shares:>10} ${price:>11.2f} ${value:>13.2f}")
            
            if value > 0:
                total_buy += value
            else:
                total_sell += abs(value)
        
        print("-"*80)
        print(f"{'Total Buys:':<42} ${total_buy:>13.2f}")
        print(f"{'Total Sells:':<42} ${total_sell:>13.2f}")
        print(f"{'Net:':<42} ${total_buy - total_sell:>13.2f}")
        
        print("\n" + "-"*60)
        print("WEIGHT CHANGES")
        print("-"*60)
        
        # Show weight changes
        print(f"\n{'Symbol':<10} {'Previous':>12} {'Target':>12} {'Change':>12}")
        print("-"*50)
        
        for trade in preview.recommended_trades:
            symbol = trade.symbol
            prev_wt = trade.prev_weight * 100
            next_wt = trade.next_weight * 100
            wt_change = (trade.next_weight - trade.prev_weight) * 100
            
            print(f"{symbol:<10} {prev_wt:>11.2f}% {next_wt:>11.2f}% {wt_change:>+11.2f}%")
    else:
        print("\nNo rebalance needed at this time.")
        print("The symphony is within its target allocation corridors.")

    print("\n" + "="*60)
    print("NOTE: This is a preview only. No trades have been placed.")
    print("To execute, use: client.deploy.rebalance(symphony_id)")
    print("="*60)
    
except ComposerAPIError as e:
    # Try to parse the error response for specific error codes
    try:
        error_data = json.loads(str(e).replace("HTTP Error 400: ", ""))
        errors = error_data.get("errors", [])
        
        for error in errors:
            error_code = error.get("code", "")
            error_title = error.get("title", "")
            
            if error_code == "dry-run-markets-closed":
                print("\n" + "="*60)
                print("MARKETS CLOSED")
                print("="*60)
                print(f"\n{error_title}")
                print("\nTrade previews are only available during market hours.")
                print("For equity symphonies, try running this during market hours (9:30 AM - 4:00 PM ET).")
                print("For crypto symphonies, previews may be available outside market hours.")
                print("="*60)
                break
            else:
                # Re-raise if it's a different error
                print(f"\nAPI Error: {error_title}")
                raise
    except (json.JSONDecodeError, KeyError):
        # If we can't parse the error, re-raise
        raise
```

**Output:**
```
Previewing rebalance for: The Holy Grail (Invest Copy) (Buy Copy)
Symphony ID: SvfHiUshxXcHUfoCyvn5

============================================================
MARKETS CLOSED
============================================================

Markets are currently closed for equity symphonies.

Trade previews are only available during market hours.
For equity symphonies, try running this during market hours (9:30 AM - 4:00 PM ET).
For crypto symphonies, previews may be available outside market hours.
============================================================
```
