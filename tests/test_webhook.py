"""Unit tests for plaidly.webhook.verify_webhook_signature."""

import hashlib
import hmac

import pytest

from plaidly import verify_webhook_signature


def _sign(payload: str, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload.encode(), digestmod=hashlib.sha256).hexdigest()


def test_valid_signature_string_payload() -> None:
    payload = '{"event":"payment.completed"}'
    secret = "whsec_test"
    sig = _sign(payload, secret)
    assert verify_webhook_signature(payload, sig, secret) is True


def test_valid_signature_bytes_payload() -> None:
    payload = b'{"event":"payment.completed"}'
    secret = "whsec_test"
    sig = _sign(payload.decode(), secret)
    assert verify_webhook_signature(payload, sig, secret) is True


def test_tampered_payload() -> None:
    secret = "whsec_test"
    sig = _sign('{"event":"payment.completed"}', secret)
    assert verify_webhook_signature('{"event":"tampered"}', sig, secret) is False


def test_wrong_secret() -> None:
    payload = '{"event":"payment.completed"}'
    sig = _sign(payload, "correct_secret")
    assert verify_webhook_signature(payload, sig, "wrong_secret") is False


def test_malformed_signature_returns_false() -> None:
    assert verify_webhook_signature("body", "notasha256sig", "secret") is False
