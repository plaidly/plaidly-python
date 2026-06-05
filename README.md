# plaidly-python

Official Python SDK for the [Plaidly](https://plaidly.io) cryptocurrency payment API.

Typed, dependency-light (`httpx` only), and aligned to the Plaidly v1 API
contract.

## Installation

```bash
pip install plaidly-python
```

## Quickstart

```python
import os
from plaidly import PlaidlyClient

client = PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"])

# Create a payment session
session = client.payment_sessions.create(
    amount=10.00,
    chain="solana",
    token="USDC",
    network="mainnet",          # "mainnet" | "testnet"
    expires_in="15m",
    metadata={"order_id": "1234"},
)

print(session.address)      # deposit address — send funds here
print(session.payment_url)  # hosted checkout URL for the payer
print(session.qr_data)      # payment URI for QR encoding

# Poll for completion (public endpoint — also usable on the checkout page)
session = client.payment_sessions.get(session.session_id)
if session.is_paid:         # True when status is "completed" or "confirmed"
    print("Paid!")
```

Every call returns a typed dataclass (`PaymentSession`, `Merchant`,
`PaymentMethodInfo`, `Rate`) — autocompletion and type checking work out of
the box. Use the context manager to close the connection pool automatically:

```python
with PlaidlyClient(api_key=os.environ["PLAIDLY_API_KEY"]) as client:
    me = client.merchants.me()
    print(me.name)
```

## Endpoints

```python
# Payment sessions
client.payment_sessions.create(amount, chain, token, network="mainnet",
                               expires_in="15m", method_id=0, metadata=None)
client.payment_sessions.get(session_id)
client.payment_sessions.create_demo(chain=None, token=None, network=None, amount=None)
client.payment_sessions.simulate(session_id)   # demo/sandbox only — instant complete

# Discovery (public)
client.payment_methods()                        # list[PaymentMethodInfo]
client.rates(symbols=["ETH", "SOL"])            # list[Rate]; stablecoins fixed at 1.0
client.faucets()                                # dict[str, str], chain:network -> URL

# Merchants
client.merchants.register(name, webhook_url=None)   # returns api_key + webhook_secret
client.merchants.me()
```

## Demo flow (no API key needed for the demo session)

```python
client = PlaidlyClient(api_key="demo")
demo = client.payment_sessions.create_demo(chain="ethereum", token="USDC", amount=5.0)
done = client.payment_sessions.simulate(demo.session_id)
assert done.is_paid
```

## Error handling

Non-2xx responses raise `PlaidlyError` with the parsed API error body. Transient
failures (network errors, 5xx) are retried up to 3 times with exponential
backoff before raising.

```python
from plaidly import PlaidlyError

try:
    client.payment_sessions.get("does-not-exist")
except PlaidlyError as e:
    print(e.status)   # HTTP status code
    print(e.code)     # application error code (int) or None
    print(e.message)  # error message
```

## Webhook verification

Plaidly signs every webhook with the `X-Plaidly-Signature` header in the form
`t=<unix>,v1=<hex>`, where the hex value is
`HMAC-SHA256(webhook_secret, "<t>.<raw_body>")`. Verification is constant-time
and enforces a 5-minute timestamp tolerance by default.

```python
import os
from plaidly import verify_webhook_signature

@app.route("/webhook", methods=["POST"])
def webhook():
    valid = verify_webhook_signature(
        payload=request.get_data(),                      # raw, unmodified body
        signature=request.headers["X-Plaidly-Signature"],
        secret=os.environ["PLAIDLY_WEBHOOK_SECRET"],     # from merchant registration
    )
    if not valid:
        return "invalid signature", 403
    # event = request.get_json()  ->  {"event_type", "session_id", "status", ...}
    return "", 204
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## API Reference

See [docs.plaidly.io](https://docs.plaidly.io) for full API documentation.
