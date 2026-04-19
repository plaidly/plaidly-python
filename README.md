# plaidly-python

Official Python SDK for the [Plaidly](https://plaidly.io) cryptocurrency payment API.

## Installation

```bash
pip install plaidly-python
```

## Usage

```python
from plaidly import PlaidlyClient
import os

client = PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"])

# Create a payment session
session = client.sessions.create(
    amount="10.00",
    currency="USDC",
    chain="solana",
    callback_url="https://yoursite.com/webhook",
)

print(session["wallet_address"])  # Send funds here
```

## Context Manager

```python
with PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"]) as client:
    merchants = client.merchants.me()
```

## Webhook Verification

```python
from plaidly import verify_webhook_signature

@app.route("/webhook", methods=["POST"])
def webhook():
    valid = verify_webhook_signature(
        request.get_data(),
        request.headers.get("X-Plaidly-Signature"),
        os.environ["PLAIDLY_WEBHOOK_SECRET"],
    )
    if not valid:
        return "Invalid signature", 401
    # handle event
    return "", 204
```

## API Reference

See [docs.plaidly.io](https://docs.plaidly.io) for full API documentation.
