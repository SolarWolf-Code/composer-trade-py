# Custom Retry Configuration

By default, the client automatically retries failed requests on rate limit (429) and server errors (500, 502, 503, 504) using exponential backoff.

## Default Behavior

- **Max retries**: 3 attempts
- **Rate limit wait**: 10 seconds (for 429 responses)
- **Server error wait**: 3 seconds (for 5xx responses)
- **Exponential backoff**: Base 2.0 (wait times double on each retry)

With the defaults, retry delays are:
- Retry 1: 10s (rate limit) / 3s (server error)
- Retry 2: 20s / 6s
- Retry 3: 40s / 12s

## Customizing Retry Config

Import `RetryConfig` and pass it to the client:

```python
from composer import ComposerClient, RetryConfig

# Use default retry behavior (recommended)
client = ComposerClient("api_key", "api_secret")
```

### Custom Wait Times

```python
from composer import ComposerClient, RetryConfig

client = ComposerClient(
    api_key="api_key",
    api_secret="api_secret",
    retry_config=RetryConfig(
        rate_limit_wait=20.0,  # Longer wait for rate limits
        server_error_wait=5.0,  # Longer wait for server errors
    )
)
```

### Disable Exponential Backoff

```python
from composer import ComposerClient, RetryConfig

client = ComposerClient(
    api_key="api_key",
    api_secret="api_secret",
    retry_config=RetryConfig(
        exponential_base=1.0,  # Constant wait times
    )
)
```

### Custom Retry Status Codes

```python
from composer import ComposerClient, RetryConfig

client = ComposerClient(
    api_key="api_key",
    api_secret="api_secret",
    retry_config=RetryConfig(
        retry_statuses={429, 500, 502},  # Only retry on these codes
    )
)
```

### Disable Retries Entirely

```python
from composer import ComposerClient

client = ComposerClient(
    api_key="api_key",
    api_secret="api_secret",
    retry_config=None,
)
```
