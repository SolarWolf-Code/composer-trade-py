"""
Example: Get first user symphony and backtest it.

This example demonstrates:
1. Fetching the user's symphonies
2. Getting the first symphony
3. Running a backtest on it

Usage:
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/first_symphony_backtest.py
"""

import os
from composer import BacktestParams, ComposerClient
from dotenv import load_dotenv


def main():
    load_dotenv()

    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    symphonies = client.user_symphonies.list_symphonies()

    if not symphonies:
        print("No symphonies found")
        return

    first = symphonies[0]
    print(f"Found {len(symphonies)} symphony(s)")
    print(f"First symphony: {first.name} (ID: {first.id})")

    print("\nRunning backtest...")
    result = client.user_symphony.backtest_symphony(first.id, BacktestParams(benchmark_tickers=["QQQ"]))

    print(result.dvm_capital["QQQ"])


if __name__ == "__main__":
    main()
