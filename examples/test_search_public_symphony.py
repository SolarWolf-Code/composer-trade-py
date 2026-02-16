"""Example file to test search and public symphony endpoints."""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: COMPOSER_API_KEY and COMPOSER_API_SECRET must be set")
        return

    client = ComposerClient(api_key, api_secret)

    print("=" * 60)
    print("Testing Search & Public Symphony Endpoints")
    print("=" * 60)

    # Test 1: Search symphonies (v1)
    print("\n1. Search Symphonies (v1):")
    print("-" * 40)
    try:
        results = client.search.search_symphonies(
            where=["and", [">", "oos_num_backtest_days", 180]],
            order_by=[["oos_sharpe_ratio", "desc"]],
            offset=0,
        )
        print(f"   Number of results: {len(results)}")
        for s in results[:3]:
            print(f"   - {s.symphony_sid}: {s.name}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 2: Search symphonies (v2 with CEL filters)
    print("\n2. Search Symphonies (v2):")
    print("-" * 40)
    try:
        results = client.search.search_symphonies_v2(
            filter="oos_sharpe_ratio > 1.5",
            order_by=[["oos_sharpe_ratio", "desc"]],
            offset=0,
        )
        print(f"   Number of results: {len(results)}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 3: Get public symphony details
    print("\n3. Get Public Symphony Details:")
    print("-" * 40)
    try:
        # First search to get a symphony ID
        results = client.search.search_symphonies(offset=0)
        if results:
            symphony_sid = results[0].symphony_sid
            symphony = client.public_symphony.get_symphony(symphony_sid)
            print(f"   Symphony: {symphony.name}")
            desc = symphony.description or ""
            print(f"   Description: {desc[:50]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: Get symphony score
    print("\n4. Get Symphony Score:")
    print("-" * 40)
    try:
        results = client.search.search_symphonies(offset=0)
        if results:
            symphony_sid = results[0].symphony_sid
            score = client.public_symphony.get_score(symphony_sid)
            print(score)
    except Exception as e:
        print(f"   Error: {e}")

    # Test 5: Get symphony versions
    print("\n5. Get Symphony Versions:")
    print("-" * 40)
    try:
        results = client.search.search_symphonies(offset=0)
        if results:
            symphony_sid = results[0].symphony_sid
            versions = client.public_symphony.get_versions(symphony_sid)
            print(f"   Number of versions: {len(versions)}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 6: Get symphony tickers
    print("\n6. Get Symphony Tickers:")
    print("-" * 40)
    try:
        results = client.search.search_symphonies(offset=0)
        if results:
            symphony_sid = results[0].symphony_sid
            tickers = client.public_symphony.get_tickers(symphony_sid)
            print(f"   Tickers: {', '.join(tickers[:5])}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
