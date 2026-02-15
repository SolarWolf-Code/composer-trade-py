"""
Example: Testing new API endpoints.

This tests the newly added endpoints:
- Public backtest endpoints
- V2 backtest endpoints
- Search v2
- Pub/sub modify
- Symphony nodes update

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_new_endpoints.py
"""

import os
from composer import (
    ComposerClient,
    BacktestParams,
    BacktestRequest,
    SymphonyDefinition,
    Root,
    Asset,
    WeightCashEqual,
    RebalanceRequest,
    SymphonyRebalanceState,
)
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    symphony_id = os.environ.get("TEST_SYMPHONY_ID", "P8npOsKAqRoPDoL6sQiE")

    print("=" * 60)
    print("PUBLIC SYMPHONY META ENDPOINT")
    print("=" * 60)

    print("\n0. POST /api/v1/public/meta/symphonies")
    try:
        meta = client.public_symphony.get_symphony_meta([symphony_id])
        print(f"   SUCCESS: Got {len(meta)} symphony(s)")
        if meta:
            print(f"   Name: {meta[0].name}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("PUBLIC BACKTEST ENDPOINTS")
    print("=" * 60)

    print("\n1. POST /api/v1/public/symphonies/{id}/backtest")
    try:
        result = client.public_symphony.backtest_symphony(symphony_id)
        print(f"   SUCCESS: Backtest completed")
        print(f"   Cumulative return: {result.stats.cumulative_return}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n2. POST /api/v1/public/backtest")
    try:
        params = BacktestParams(capital=10000)
        result = client.public_symphony.backtest(params=params)
        print(f"   SUCCESS: Standalone backtest completed")
        print(f"   Cumulative return: {result.stats.cumulative_return}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("V2 BACKTEST ENDPOINTS")
    print("=" * 60)

    print("\n3. POST /api/v2/public/symphonies/{id}/backtest (v2)")
    try:
        result = client.public_symphony.backtest_symphony_v2(symphony_id)
        print(f"   SUCCESS: V2 backtest completed")
        print(f"   Cumulative return: {result.stats.cumulative_return}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n4. POST /api/v2/symphonies/{id}/backtest (v2, authenticated)")
    try:
        result = client.user_symphony.backtest_symphony_v2(symphony_id)
        print(f"   SUCCESS: V2 backtest completed")
        print(f"   Cumulative return: {result.stats.cumulative_return}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n5. POST /api/v2/backtest (v2 generic)")
    try:
        symphony = Root(
            name="Test Strategy - Python SDK",
            description="A test symphony created via Python SDK",
            rebalance="daily",
            children=[
                WeightCashEqual(children=[Asset(ticker="AAPL", name="Apple Inc", exchange="XNAS")])
            ],
        )
        request = BacktestRequest(symphony=SymphonyDefinition(raw_value=symphony), capital=10000)
        result = client.backtest.run_v2(request)
        print(f"   SUCCESS: V2 backtest completed")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n6. POST /api/v2/public/backtest (v2 public)")
    try:
        symphony = Root(
            name="Test Strategy - Python SDK",
            description="A test symphony created via Python SDK",
            rebalance="daily",
            children=[
                WeightCashEqual(children=[Asset(ticker="AAPL", name="Apple Inc", exchange="XNAS")])
            ],
        )
        request = BacktestRequest(symphony=SymphonyDefinition(raw_value=symphony), capital=10000)
        result = client.backtest.run_public_v2(request)
        print(f"   SUCCESS: V2 public backtest completed")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("SEARCH V2 ENDPOINT")
    print("=" * 60)

    print("\n7. POST /api/v1/public/search/symphonies-v2")
    try:
        results = client.search.search_symphonies_v2(filter="oos_sharpe_ratio > 1.0", offset=0)
        print(f"   SUCCESS: Found {len(results)} symphonies")
        if results:
            print(f"   First result: {results[0].name}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("REBALANCE ENDPOINT")
    print("=" * 60)

    print("\n8. POST /api/v2/rebalance")
    try:
        request = RebalanceRequest(
            symphonies={symphony_id: SymphonyRebalanceState(cash=10000.0, shares={})}, dry_run=True
        )
        result = client.backtest.rebalance(request)
        print(f"   SUCCESS: Rebalance completed")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("SYMPHONY NODES UPDATE")
    print("=" * 60)

    print("\n9. PATCH /api/v1/symphonies/{id}/versions/{vid}/score/nodes")
    try:
        versions = client.user_symphony.get_versions(symphony_id)
        if versions:
            version_id = versions[0].version_id
            result = client.user_symphony.update_symphony_nodes(
                symphony_id=symphony_id, version_id=version_id, updates=[]
            )
            print(f"   SUCCESS: Nodes updated")
            print(f"   Result: {result}")
        else:
            print("   SKIP: No versions available")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
