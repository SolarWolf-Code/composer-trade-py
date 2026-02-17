"""
Example: Testing Watchlist and Modify endpoints.

This demonstrates the POST endpoints for:
- Adding symphonies to watchlist
- Removing symphonies from watchlist
- Modifying a single symphony (find and replace ticker)
- Bulk modifying user symphonies

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_watchlist_and_modify.py
"""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


SYMPHONY_IDS = [
    "fk6VGRDAAgiH120TfUPS",
    "Kw6qGNXUGEeansidJVwl",
    "njJ8aCEnJVkrWDxBiI9v",
]


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    print("=" * 60)
    print("WATCHLIST ENDPOINTS")
    print("=" * 60)

    print("\n1. Get current watchlist")
    try:
        watchlist = client.watchlist.get_watchlist()
        print(f"   SUCCESS: Found {len(watchlist)} items in watchlist")
        for item in watchlist[:3]:
            print(f"   - {item.name}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n2. Add symphonies to watchlist")
    for symphony_id in SYMPHONY_IDS:
        try:
            result = client.watchlist.add_to_watchlist(symphony_id)
            print(f"   SUCCESS: Added '{result.name}' to watchlist")
        except Exception as e:
            print(f"   ERROR adding {symphony_id}: {e}")

    print("\n3. Get updated watchlist")
    try:
        watchlist = client.watchlist.get_watchlist()
        print(f"   SUCCESS: Found {len(watchlist)} items in watchlist")
    except Exception as e:
        print(f"   ERROR: {e}")

    
    print("\n4. Remove symphonies from watchlist")
    for symphony_id in SYMPHONY_IDS:
        try:
            client.watchlist.remove_from_watchlist(symphony_id)
            print(f"   SUCCESS: Removed {symphony_id} from watchlist")
        except Exception as e:
            print(f"   ERROR removing {symphony_id}: {e}")

    print("\n5. Get final watchlist")
    try:
        watchlist = client.watchlist.get_watchlist()
        print(f"   SUCCESS: Found {len(watchlist)} items in watchlist")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("MODIFY SYMPHONY ENDPOINTS")
    print("=" * 60)

    print("\n6. Modify a single symphony (find and replace ticker)")
    symphony_id = SYMPHONY_IDS[0]
    try:
        result = client.user_symphony.modify_symphony(
            symphony_id=symphony_id, old_ticker="SPY", new_ticker="QQQ"
        )
        print(f"   SUCCESS: Modified symphony")
        print(f"   - symphony_id: {result.symphony_id}")
        print(f"   - version_id: {result.version_id}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n7. Bulk modify user symphonies (find and replace ticker)")
    try:
        result = client.user_symphonies.bulk_modify_symphonies(old_ticker="SPY", new_ticker="QQQ")
        print(f"   SUCCESS: Bulk modify completed")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
