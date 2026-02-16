"""
Example: Testing User endpoints.

This demonstrates user endpoints:
- get_jwt
- get_profile
- get_agreement_status

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_user_endpoints.py
"""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    print("\n" + "=" * 60)
    print("USER ENDPOINTS")
    print("=" * 60)

    # Test 1: get_jwt
    print("\n1. get_jwt")
    try:
        jwt = client.user.get_jwt()
        print(f"   SUCCESS: Got JWT token")
        print(f"   - Token: {jwt.token[:20]}...")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get_profile
    print("\n2. get_profile")
    try:
        profile = client.user.get_profile()
        print(f"   SUCCESS: Got user profile")
        print(f"   - Name: {profile.first_name} {profile.last_name}")
        print(f"   - Email: {profile.phone_number}")
        print(f"   - Country: {profile.country}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_agreement_status
    print("\n3. get_agreement_status (test-agreement)")
    try:
        status = client.user.get_agreement_status("test-agreement")
        print(f"   SUCCESS: Agreement status retrieved")
        print(f"   - Has agreed: {status.has_agreed}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
