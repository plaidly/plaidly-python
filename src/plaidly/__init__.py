"""Plaidly Python SDK — official client for the Plaidly crypto payment API."""

from .client import PlaidlyClient
from .errors import PlaidlyError
from .models import (
    Merchant,
    PaymentMethod,
    PaymentMethodInfo,
    PaymentSession,
    Rate,
)
from .webhook import (
    compute_signature,
    verify_webhook_signature,
)

__all__ = [
    "PlaidlyClient",
    "PlaidlyError",
    "Merchant",
    "PaymentMethod",
    "PaymentMethodInfo",
    "PaymentSession",
    "Rate",
    "verify_webhook_signature",
    "compute_signature",
]
__version__ = "0.2.0"
