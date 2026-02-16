"""
Example: Testing AI Agents endpoints.

This demonstrates AI agents endpoints:
- list
- get
- get_executions

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_ai_agents_endpoints.py
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

    # Get account ID from env or fetch from accounts list
    account_id = os.environ.get("COMPOSER_ACCOUNT_ID")

    if not account_id:
        print("\nFetching accounts list to get account_id...")
        try:
            accounts_response = client.accounts.list()
            if accounts_response.accounts:
                account_id = accounts_response.accounts[0].account_uuid
                print(f"Using first account: {account_id}")
            else:
                print("ERROR: No accounts found")
                return
        except Exception as e:
            print(f"ERROR: {e}")
            return

    print("\n" + "=" * 60)
    print("AI AGENTS ENDPOINTS")
    print("=" * 60)

    # Test 1: list
    print("\n1. list")
    try:
        agents = client.ai_agents.list(broker_account_id=account_id)
        print(f"   SUCCESS: Found {len(agents.agents)} AI agents")
        for agent in agents.agents[:3]:
            print(f"   - {agent.name}: {agent.status}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get (requires agent_id)
    print("\n2. get")
    try:
        agents = client.ai_agents.list(broker_account_id=account_id, limit=1)
        if agents.agents:
            agent_id = agents.agents[0].ai_agent_sid
            agent = client.ai_agents.get(agent_id)
            print(f"   SUCCESS: Got agent {agent.name}")
            print(f"   - Status: {agent.status}")
            print(f"   - Schedule: {agent.schedule_cron}")
        else:
            print("   SKIPPED: No agents found")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_executions (requires agent_id)
    print("\n3. get_executions")
    try:
        agents = client.ai_agents.list(broker_account_id=account_id, limit=1)
        if agents.agents:
            agent_id = agents.agents[0].ai_agent_sid
            executions = client.ai_agents.get_executions(agent_id)
            print(f"   SUCCESS: Found {len(executions.executions)} executions")
            for ex in executions.executions[:3]:
                print(f"   - {ex.status}: {ex.started_at}")
        else:
            print("   SKIPPED: No agents found")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
