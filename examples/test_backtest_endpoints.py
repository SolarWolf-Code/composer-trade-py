"""
Example: Testing all Backtest API endpoints.

This demonstrates all the new endpoints added from the backtest-swagger.json:
- Public endpoints (no auth required)
- Authenticated endpoints

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    # Replace TEST_SYMPHONY_ID with a valid symphony ID
    export TEST_SYMPHONY_ID="your-symphony-id"

    python examples/test_backtest_endpoints.py
"""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


def main():
    # Get credentials from environment
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    # Get test symphony ID from environment or use a default
    symphony_id = os.environ.get("TEST_SYMPHONY_ID", "P8npOsKAqRoPDoL6sQiE")

    # Initialize client
    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    print("=" * 60)
    print("PUBLIC ENDPOINTS (No Auth)")
    print("=" * 60)

    # 1. Get indicators (public)
    print("\n1. GET /api/v1/public/symphony-scores/indicators")
    try:
        indicators = client.public_symphony.get_indicators()
        print(f"   SUCCESS: Found {len(indicators)} indicators")
        print(indicators)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 2. Get symphony meta
    print("\n2. POST /api/v1/public/meta/symphonies")
    try:
        meta = client.public_symphony.get_symphony_meta([symphony_id])
        print(f"   SUCCESS: Found {len(meta)} symphonies")
        print(meta)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 3. Get symphony details
    print(f"\n3. GET /api/v1/public/symphonies/{symphony_id}")
    try:
        symphony = client.public_symphony.get_symphony(symphony_id)
        print(f"   SUCCESS: {symphony.name}")
        print(symphony)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 4. Get symphony versions
    print(f"\n4. GET /api/v1/public/symphonies/{symphony_id}/versions")
    try:
        versions = client.public_symphony.get_versions(symphony_id)
        print(f"   SUCCESS: Found {len(versions)} versions")
        print(versions)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 5. Get symphony score
    print(f"\n5. GET /api/v1/public/symphonies/{symphony_id}/score")
    try:
        score = client.public_symphony.get_score(symphony_id)
        print(f"   SUCCESS: Score name={score.name}")
        print(score)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 6. Get version score
    print(f"\n6. GET /api/v1/public/symphonies/{symphony_id}/versions/{{version_id}}/score")
    try:
        versions = client.public_symphony.get_versions(symphony_id)
        if versions:
            version_id = versions[0].version_id
            score = client.public_symphony.get_version_score(symphony_id, version_id)
            print(f"   SUCCESS: Version score name={score.name}")
            print(score)
        else:
            print("   SKIP: No versions available")
    except Exception as e:
        print(f"   ERROR: {e}")

    # 7. Get tickers
    print(f"\n7. GET /api/v1/public/symphonies/{symphony_id}/tickers")
    try:
        tickers = client.public_symphony.get_tickers(symphony_id)
        print(f"   SUCCESS: Found {len(tickers)} tickers")
        print(tickers)
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("AUTHENTICATED ENDPOINTS")
    print("=" * 60)

    # 8. Get indicators (authenticated)
    print("\n8. GET /api/v1/symphony-scores/indicators")
    try:
        indicators = client.user_symphony.get_indicators()
        print(f"   SUCCESS: Found {len(indicators)} indicators")
        print(indicators)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 9. Get symphony (authenticated)
    print(f"\n9. GET /api/v1/symphonies/{symphony_id}")
    try:
        symphony = client.user_symphony.get_symphony(symphony_id)
        print(f"   SUCCESS: {symphony.name}")
        print(symphony)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 10. Get versions (authenticated)
    print(f"\n10. GET /api/v1/symphonies/{symphony_id}/versions")
    try:
        versions = client.user_symphony.get_versions(symphony_id)
        print(f"   SUCCESS: Found {len(versions)} versions")
        print(versions)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 11. Get score (authenticated)
    print(f"\n11. GET /api/v1/symphonies/{symphony_id}/score")
    try:
        score = client.user_symphony.get_score(symphony_id)
        print(f"   SUCCESS: Score name={score.name}")
        print(score)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 12. Get version score (authenticated)
    print(f"\n12. GET /api/v1/symphonies/{symphony_id}/versions/{{version_id}}/score")
    try:
        versions = client.user_symphony.get_versions(symphony_id)
        if versions:
            version_id = versions[0].version_id
            score = client.user_symphony.get_version_score(symphony_id, version_id)
            print(f"   SUCCESS: Version score name={score.name}")
            print(score)
        else:
            print("   SKIP: No versions available")
    except Exception as e:
        print(f"   ERROR: {e}")

    # 13. List user's symphonies
    print("\n13. GET /api/v1/user/symphonies")
    try:
        symphonies = client.user_symphonies.list_symphonies()
        print(f"   SUCCESS: Found {len(symphonies)} symphonies")
        for symphony in symphonies[:3]:
            print(symphony)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 14. List drafts
    print("\n14. GET /api/v1/user/symphonies/drafts")
    try:
        drafts = client.user_symphonies.list_drafts()
        print(f"   SUCCESS: Found {len(drafts)} drafts")
        # print(drafts)
        for draft in drafts[:3]:
            print(draft)
    except Exception as e:
        print(f"   ERROR: {e}")

    # 15. Get watchlist
    print("\n15. GET /api/v1/watchlist")
    try:
        watchlist = client.watchlist.get_watchlist()
        print(f"   SUCCESS: Found {len(watchlist)} watchlist items")
        for item in watchlist[:3]:
            print(item)
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
