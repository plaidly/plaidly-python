"""Webhook signature verification for Plaidly events."""

from __future__ import annotations

import hashlib
import hmac


def verify_webhook_signature(payload: bytes | str, signature: str, secret: str) -> bool:
    """Verify that an incoming webhook came from Plaidly.

    Plaidly sets the ``X-Plaidly-Signature`` header to
    ``sha256=<hex>`` where the hex string is
    ``HMAC-SHA256(secret, raw_body)``.

    Args:
        payload: Raw request body (bytes or str — must be the *unmodified* body).
        signature: Value of the ``X-Plaidly-Signature`` header.
        secret: Your webhook secret from the Plaidly dashboard.

    Returns:
        ``True`` if the signature is valid; ``False`` otherwise.

    Example::

        from plaidly import verify_webhook_signature

        is_valid = verify_webhook_signature(
            payload=request.body,
            signature=request.headers["X-Plaidly-Signature"],
            secret="whsec_...",
        )
        if not is_valid:
            return HttpResponse(status=403)
    """
    if isinstance(payload, str):
        payload = payload.encode()

    expected = "sha256=" + hmac.new(
        secret.encode(), payload, digestmod=hashlib.sha256
    ).hexdigest()

    # Use hmac.compare_digest for timing-safe comparison
    try:
        return hmac.compare_digest(signature, expected)
    except (TypeError, ValueError):
        return False
