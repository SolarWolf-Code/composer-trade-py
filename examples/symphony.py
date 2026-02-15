"""
Example: Symphony management.

This example demonstrates:
1. Creating a new symphony using programmatic node building
2. Getting the EDN (score)
3. Updating the symphony
4. Listing all versions
5. Getting a specific version's EDN
6. Copying the symphony
7. Deleting both the copy and original
"""

import os
from dotenv import load_dotenv

from composer import ComposerClient
from composer.models.symphony import (
    CreateSymphonyRequest,
    AssetClass,
)
from composer.models.common.symphony import (
    Root,
    Asset,
    WeightCashEqual,
)

load_dotenv()


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    # Build a simple symphony programmatically
    print("Building symphony programmatically...")

    # Create the request with both metadata and trading logic
    create_request = CreateSymphonyRequest(
        name="Example Symphony - Python SDK Test",
        asset_class=AssetClass.EQUITIES,
        description="A test symphony created via Python SDK",
        color="#FF6B6B",
        hashtag="#TEST",
        symphony=Root(
            name="Example Symphony - Python SDK Test",
            description="A test symphony created via Python SDK",
            rebalance="daily",
            children=[
                WeightCashEqual(
                    children=[Asset(ticker="AAPL", name="Apple Inc", exchange="XNAS")]
                )
            ],
        ),
    )

    print("=" * 60)
    print("1. CREATE SYMPHONY")
    print("=" * 60)
    print(f"Creating symphony: {create_request.name}\n")

    created = client.symphony.create_symphony(create_request)
    symphony_id = created.symphony_id
    print(f"Created symphony with ID: {symphony_id}")
    print(f"Version ID: {created.version_id}\n")

    print("=" * 60)
    print("2. GET SYMPHONY EDN (SCORE)")
    print("=" * 60)
    print(f"Fetching EDN for symphony: {symphony_id}\n")

    score = client.symphony.score_symphony(symphony_id)
    print(f"  Name: {score.name}")
    print(f"  Description: {score.description}")
    print(f"  Rebalance: {score.rebalance}")
    print(f"  Root Step Type: {score.step}")
    print()

    print("=" * 60)
    print("3. UPDATE SYMPHONY")
    print("=" * 60)
    print(f"Updating symphony: {symphony_id}\n")

    # Create updated request with new metadata
    update_request = CreateSymphonyRequest(
        name="Example Symphony - Python SDK Test (Updated)",
        asset_class=AssetClass.EQUITIES,
        description="This symphony was updated via Python SDK",
        color="#39D088",
        hashtag="#UPDATED",
        # No symphony field means we're only updating metadata, not the trading logic
    )

    updated = client.symphony.update_symphony(symphony_id, update_request)
    print(f"  Updated version ID: {updated.version_id}")
    print(f"  Previous version ID: {updated.existing_version_id}")
    print()

    print("=" * 60)
    print("4. LIST ALL VERSIONS")
    print("=" * 60)
    print(f"Listing versions for symphony: {symphony_id}\n")

    versions = client.symphony.list_symphony_versions(symphony_id)
    print(f"  Total versions: {len(versions)}")
    for i, version in enumerate(versions):
        print(
            f"    {i + 1}. Version ID: {version.version_id} - Created: {version.created_at}"
        )
    print()

    print("=" * 60)
    print("5. GET SPECIFIC VERSION EDN")
    print("=" * 60)
    if versions:
        first_version_id = versions[0].version_id
        print(f"Fetching EDN for version: {first_version_id}\n")

        version_score = client.symphony.get_symphony_version_score(
            symphony_id, first_version_id
        )
        print(f"  Version {first_version_id}:")
        print(f"    Name: {version_score.name}")
        print(f"    Rebalance: {version_score.rebalance}")
        print()
    else:
        print("  No versions found.\n")

    print("=" * 60)
    print("6. COPY SYMPHONY")
    print("=" * 60)
    print(f"Copying symphony: {symphony_id}\n")

    copied = client.symphony.copy_symphony(symphony_id)
    copy_id = copied.symphony_id
    print(f"  Copied symphony ID: {copy_id}")
    print(f"  Copy version ID: {copied.version_id}")
    print()

    print("=" * 60)
    print("7. DELETE BOTH SYMPHONIES")
    print("=" * 60)

    print(f"Deleting copy: {copy_id}...")
    client.symphony.delete_symphony(copy_id)
    print(f"  Deleted copy: {copy_id}\n")

    print(f"Deleting original: {symphony_id}...")
    client.symphony.delete_symphony(symphony_id)
    print(f"  Deleted original: {symphony_id}\n")

    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print("Successfully created, updated, copied, and deleted symphonies.")


if __name__ == "__main__":
    main()
