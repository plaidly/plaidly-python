# plaidly-python

Official Python SDK for the [Plaidly](https://plaidly.io) cryptocurrency payment API.

Types and the low-level HTTP client are auto-generated from the Plaidly
OpenAPI 3.1 spec with
[`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client).
The high-level `PlaidlyClient` and the `verify_webhook_signature` helper
are hand-written wrappers that add retries, typed errors, and ergonomic
groupings.

## Installation

```bash
pip install plaidly-python
```

## Usage

```python
from plaidly import (
    PlaidlyClient,
    CreatePaymentSessionRequest,
    PaymentMethod,
)
import os

client = PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"])

session = client.payment_sessions.create(
    CreatePaymentSessionRequest(
        amount=10.0,
        expires_in="15m",
        payment_method=PaymentMethod(
            method_id=0, chain="solana", token="USDC", network="mainnet",
        ),
    )
)

print(session.address)  # Send funds here
```

## Context Manager

```python
with PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"]) as client:
    merchant = client.merchants.me()
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
    return "", 204
```

## Escape hatch — generated client

For endpoints not yet exposed on `PlaidlyClient`, use the raw
`AuthenticatedClient` from [openapi-python-client]:

```python
from plaidly.generated.api.wallets import list_wallets

client = PlaidlyClient(api_key="...").raw
wallets = list_wallets.sync(client=client)
```

## Regenerating from the spec

The committed copy of the Plaidly spec lives at `spec/openapi.yaml`.

```bash
make generate                                   # default
make generate SPEC=path/to/openapi.yaml
make generate OAPI_PY_CLIENT_VERSION=0.24.3
```

Generated output: `src/plaidly/generated/`. Do not edit by hand.

Pinned versions:

- `openapi-python-client==0.24.3`

## API Reference

See [docs.plaidly.io](https://docs.plaidly.io) for full API documentation.
