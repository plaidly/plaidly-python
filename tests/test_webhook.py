"""Unit tests for plaidly.webhook signature verification."""

import hashlib
import hmac
import time

from plaidly import compute_signature, verify_webhook_signature

GOLDEN_SECRET = "whsec_test_secret"
GOLDEN_TS = 1700000000
GOLDEN_BODY = (
    '{"event_type":"payment_session.completed",'
    '"session_id":"ps_123","status":"completed","amount":10.5,'
    '"currency":"USDC","chain":"solana","network":"mainnet",'
    f'"timestamp":{GOLDEN_TS}}}'
)


def _expected(body: str, secret: str, ts: int) -> str:
    msg = f"{ts}.{body}".encode("utf-8")
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def _header(body: str, secret: str, ts: int) -> str:
    return f"t={ts},v1={_expected(body, secret, ts)}"


def test_golden_vector() -> None:
    expected_hex = _expected(GOLDEN_BODY, GOLDEN_SECRET, GOLDEN_TS)
    assert compute_signature(GOLDEN_BODY, GOLDEN_SECRET, GOLDEN_TS) == expected_hex
    header = f"t={GOLDEN_TS},v1={expected_hex}"
    assert (
        verify_webhook_signature(
            GOLDEN_BODY, header, GOLDEN_SECRET, tolerance_seconds=0
        )
        is True
    )


def test_valid_signature_bytes_payload() -> None:
    secret = "whsec_test"
    ts = int(time.time())
    header = _header(GOLDEN_BODY, secret, ts)
    assert verify_webhook_signature(GOLDEN_BODY.encode(), header, secret) is True


def test_tampered_payload() -> None:
    secret = "whsec_test"
    header = _header(GOLDEN_BODY, secret, GOLDEN_TS)
    tampered = GOLDEN_BODY.replace("completed", "failed")
    assert (
        verify_webhook_signature(tampered, header, secret, tolerance_seconds=0)
        is False
    )


def test_wrong_secret() -> None:
    header = _header(GOLDEN_BODY, "correct_secret", GOLDEN_TS)
    assert (
        verify_webhook_signature(
            GOLDEN_BODY, header, "wrong_secret", tolerance_seconds=0
        )
        is False
    )


def test_malformed_signature_returns_false() -> None:
    assert verify_webhook_signature("body", "notasignature", "secret") is False
    assert verify_webhook_signature("body", "", "secret") is False
    assert verify_webhook_signature("body", "t=123", "secret") is False


def test_expired_timestamp_rejected() -> None:
    secret = "whsec_test"
    old_ts = int(time.time()) - 600
    header = _header(GOLDEN_BODY, secret, old_ts)
    assert (
        verify_webhook_signature(GOLDEN_BODY, header, secret, tolerance_seconds=300)
        is False
    )


def test_fresh_timestamp_accepted() -> None:
    secret = "whsec_test"
    ts = int(time.time()) - 10
    header = _header(GOLDEN_BODY, secret, ts)
    assert (
        verify_webhook_signature(GOLDEN_BODY, header, secret, tolerance_seconds=300)
        is True
    )


def test_non_numeric_timestamp_rejected() -> None:
    secret = "whsec_test"
    sig = _expected(GOLDEN_BODY, secret, GOLDEN_TS)
    header = f"t=notanumber,v1={sig}"
    assert verify_webhook_signature(GOLDEN_BODY, header, secret) is False
