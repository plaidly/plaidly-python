"""Webhook signature verification for Plaidly events."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

DEFAULT_TOLERANCE_SECONDS = 300


def _parse_signature_header(header: str) -> tuple[Optional[str], Optional[str]]:
    """Parse a ``t=<unix>,v1=<hex>`` signature header into its parts."""
    timestamp: Optional[str] = None
    signature: Optional[str] = None
    for part in header.split(","):
        key, _, value = part.strip().partition("=")
        if key == "t":
            timestamp = value
        elif key == "v1":
            signature = value
    return timestamp, signature


def compute_signature(payload: bytes | str, secret: str, timestamp: int | str) -> str:
    """Compute the hex ``v1`` signature for a payload.

    The signed message is ``"<timestamp>.<raw_body>"`` and the signature is
    ``HMAC-SHA256(secret, message)``.
    """
    if isinstance(payload, bytes):
        body = payload.decode("utf-8")
    else:
        body = payload
    message = f"{timestamp}.{body}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_webhook_signature(
    payload: bytes | str,
    signature: str,
    secret: str,
    tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
) -> bool:
    """Verify that an incoming webhook came from Plaidly.

    Plaidly sets the ``X-Plaidly-Signature`` header to
    ``t=<unix>,v1=<hex>`` where the hex value is
    ``HMAC-SHA256(secret, "<t>.<raw_body>")``.

    The comparison is constant-time and the signed timestamp must be within
    ``tolerance_seconds`` of the current time (replay protection). Pass
    ``tolerance_seconds=0`` to disable the freshness check.

    Args:
        payload: Raw request body (bytes or str — must be the *unmodified* body).
        signature: Value of the ``X-Plaidly-Signature`` header.
        secret: Your webhook secret from the merchant registration response.
        tolerance_seconds: Max allowed clock skew in seconds (default: 300).

    Returns:
        ``True`` if the signature is valid and fresh; ``False`` otherwise.

    Example::

        from plaidly import verify_webhook_signature

        is_valid = verify_webhook_signature(
            payload=request.body,
            signature=request.headers["X-Plaidly-Signature"],
            secret=os.environ["PLAIDLY_WEBHOOK_SECRET"],
        )
        if not is_valid:
            return HttpResponse(status=403)
    """
    if not signature or not secret:
        return False

    timestamp, provided = _parse_signature_header(signature)
    if timestamp is None or provided is None:
        return False

    if tolerance_seconds > 0:
        try:
            ts = int(timestamp)
        except (TypeError, ValueError):
            return False
        if abs(time.time() - ts) > tolerance_seconds:
            return False

    expected = compute_signature(payload, secret, timestamp)
    try:
        return hmac.compare_digest(provided, expected)
    except (TypeError, ValueError):
        return False
