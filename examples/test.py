from composer import ComposerClient
from composer.models.common.symphony import Asset
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get symphony score
score = client.user_symphony.get_score("P8npOsKAqRoPDoL6sQiE")


# Remove name from all asset classes
def remove_asset_names(node):
    """Recursively remove name from all Asset nodes."""
    if isinstance(node, Asset):
        node.name = None
    elif hasattr(node, "children") and node.children:
        for child in node.children:
            remove_asset_names(child)


# Process the score
if score.children:
    for child in score.children:
        remove_asset_names(child)

print("Updated score (names removed):")

# Create a new symphony with the updated score
result = client.user_symphony.create_symphony(
    name=score.name + " (No Asset Names)",
    description=score.description,
    color="#000000",
    hashtag="#modified",
    symphony=score,
)
print(f"\nCreated new symphony: {result.symphony_id}")
