"""
Example: Testing Market Data endpoints.

This demonstrates market data endpoints:
- get_snapshot
- get_custom_bars
- get_market_overview
- get_top_movers
- get_options_chain
- get_options_contract
- get_options_overview

And quotes (POST):
- get_quotes

Usage:
    python examples/test_market_data_endpoints.py
"""

from composer import ComposerClient


def main():
    client = ComposerClient(api_key="test", api_secret="test")

    print("\n" + "=" * 60)
    print("MARKET DATA ENDPOINTS")
    print("=" * 60)

    # Test 1: get_snapshot
    print("\n1. get_snapshot (AAPL)")
    try:
        snapshot = client.market_data.get_snapshot("AAPL")
        print(f"   SUCCESS: Symbol: {snapshot.symbol}")
        print(f"   - Last price: ${snapshot.last_trade.price if snapshot.last_trade else 'N/A'}")
        print(f"   - Today's change: {snapshot.todays_change}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get_custom_bars
    print("\n2. get_custom_bars (AAPL)")
    try:
        bars = client.market_data.get_custom_bars("AAPL", range_preset="1-month")
        print(f"   SUCCESS: Got {len(bars.data)} bars")
        if bars.data:
            print(f"   - Latest close: ${bars.data[-1].close}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_market_overview
    print("\n3. get_market_overview (AAPL)")
    try:
        overview = client.market_data.get_market_overview("AAPL")
        print(f"   SUCCESS: {overview.name}")
        print(f"   - Asset type: {overview.asset_type}")
        print(f"   - Sector: {overview.sector}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 4: get_top_movers
    print("\n4. get_top_movers")
    try:
        movers = client.market_data.get_top_movers()
        print(f"   SUCCESS: Got {len(movers.top_movers)} top movers")
        for m in movers.top_movers[:3]:
            print(f"   - {m.symbol}: ${m.last_price} ({m.todays_change_percent:+.2f}%)")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 5: get_options_overview
    print("\n5. get_options_overview (AAPL)")
    try:
        overview = client.market_data.get_options_overview("AAPL")
        print(f"   SUCCESS: Symbol: {overview.symbol}")
        print(f"   - Expirations: {len(overview.calendar)}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 6: get_options_chain
    print("\n6. get_options_chain (AAPL)")
    try:
        chain = client.market_data.get_options_chain("AAPL", limit=5)
        print(f"   SUCCESS: Got {len(chain.results)} options")
        for c in chain.results[:3]:
            print(f"   - {c.symbol}: ${c.last_trade.price if c.last_trade else 'N/A'}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 7: get_quotes (POST - no auth required)
    print("\n7. get_quotes (AAPL, CRYPTO::BTC//USD)")
    try:
        quotes = client.quotes.get_quotes(["EQUITIES::AAPL//USD", "CRYPTO::BTC//USD"])
        print(f"   SUCCESS: Got {len(quotes)} quotes")
        for symbol, quote in quotes.items():
            print(f"   - {symbol}: ${quote.price}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
