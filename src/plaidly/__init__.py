"""Plaidly Python SDK — official client for the Plaidly crypto payment API.

Types and the low-level HTTP client are auto-generated from the Plaidly
OpenAPI 3.1 spec (see ``spec/openapi.yaml``, regenerate with
``make generate``). The :class:`PlaidlyClient` class in this package is a
hand-written wrapper that adds retries, typed errors, and ergonomic
groupings of related endpoints.
"""

from .client import (
    CreatePaymentSessionRequest,
    CreateWalletRequest,
    Merchant,
    PaymentMethod,
    PaymentSession,
    PlaidlyClient,
    PlaidlyError,
    Payout,
    RegisterMerchantRequest,
    RequestPayoutRequest,
    Transaction,
    Wallet,
)
from .webhook import verify_webhook_signature

__all__ = [
    "PlaidlyClient",
    "PlaidlyError",
    "verify_webhook_signature",
    "CreatePaymentSessionRequest",
    "CreateWalletRequest",
    "Merchant",
    "PaymentMethod",
    "PaymentSession",
    "Payout",
    "RegisterMerchantRequest",
    "RequestPayoutRequest",
    "Transaction",
    "Wallet",
]
__version__ = "0.1.0"
