# Copy a symphony programatically

```python
"""
Copy a symphony programatically
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

original_symphony = "VPVpD1SoqR5ykVu4NdWS" # Holy Grail

result = client.user_symphony.copy_symphony(original_symphony)

print(f"Created {result.symphony_id} from {original_symphony}")
```

**Output:**
```
Created cgmP4k7S22jfnLwFGCU5 from VPVpD1SoqR5ykVu4NdWS
```
