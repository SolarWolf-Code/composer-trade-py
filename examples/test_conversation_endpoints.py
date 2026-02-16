"""
Example: Testing Conversation endpoints.

This demonstrates all conversation endpoints:
- create
- get_starting_points
- get
- send_message
- send_feedback
- cancel_processing_message
- upload_file
- update_state

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_conversation_endpoints.py
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
    print("CONVERSATION ENDPOINTS")
    print("=" * 60)

    # Get account ID
    print("\n0. Getting account ID...")
    account_id = os.environ.get("COMPOSER_ACCOUNT_ID")
    if not account_id:
        try:
            accounts_response = client.accounts.list()
            if accounts_response.accounts:
                account_id = accounts_response.accounts[0].account_uuid
                print(f"   Using first account: {account_id}")
            else:
                print("   ERROR: No accounts found")
                return
        except Exception as e:
            print(f"   ERROR: {e}")
            return

    # Test 1: get_starting_points
    print("\n1. get_starting_points")
    try:
        starting_points = client.conversation.get_starting_points()
        print(f"   SUCCESS: Got {len(starting_points.starting_points)} starting points")
        for sp in starting_points.starting_points[:3]:
            print(f"   - {sp.title}: {sp.text[:50]}...")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: create conversation
    print("\n2. create (new conversation)")
    conversation_id = None
    try:
        response = client.conversation.create(
            account_id=account_id, text="Hello, I want to learn about investing"
        )
        conversation_id = response.id
        print(f"   SUCCESS: Created conversation {conversation_id}")
        print(f"   Location: {response.location}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get conversation
    if conversation_id:
        print("\n3. get (conversation details)")
        try:
            conversation = client.conversation.get(conversation_id)
            print(f"   SUCCESS: Got conversation {conversation.id}")
            print(f"   Account ID: {conversation.account_id}")
            print(f"   Messages: {len(conversation.messages)}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n3. get - SKIPPED (no conversation_id)")

    # Test 4: send_message
    message_id = None
    if conversation_id:
        print("\n4. send_message")
        try:
            response = client.conversation.send_message(
                conversation_id=conversation_id, text="What are some good tech stocks to invest in?"
            )
            print(f"   SUCCESS: Message sent")
            if response.message_id:
                message_id = response.message_id
                print(f"   Message ID: {message_id}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n4. send_message - SKIPPED (no conversation_id)")

    # Test 5: send_feedback
    if message_id and conversation_id:
        print("\n5. send_feedback")
        try:
            response = client.conversation.send_feedback(
                conversation_id=conversation_id,
                message_id=message_id,
                action_type="like",
                details={"rating": 5},
            )
            print(f"   SUCCESS: Feedback sent")
            print(f"   Response: {response}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n5. send_feedback - SKIPPED (no message_id)")

    # Test 6: cancel_processing_message
    # This is typically used to cancel a message that's still processing
    print("\n6. cancel_processing_message")
    print("   SKIPPED (not applicable for completed messages)")

    # Test 7: upload_file
    # Requires file upload support - skipped for now
    print("\n7. upload_file")
    print("   SKIPPED (file upload not implemented)")

    # Test 8: update_state
    if message_id and conversation_id:
        print("\n8. update_state")
        try:
            response = client.conversation.update_state(
                conversation_id=conversation_id, message_uuid=message_id
            )
            print(f"   SUCCESS: State updated")
            print(f"   Response: {response}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n8. update_state - SKIPPED (no message_id)")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
