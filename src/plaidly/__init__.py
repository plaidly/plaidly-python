"""Plaidly Python SDK — official client for the Plaidly crypto payment API."""

from .client import PlaidlyClient
from .webhook import verify_webhook_signature

__all__ = ["PlaidlyClient", "verify_webhook_signature"]
__version__ = "0.1.0"
