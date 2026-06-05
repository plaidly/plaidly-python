"""Per-endpoint and error-mapping tests using an httpx MockTransport."""

from __future__ import annotations

import json
from typing import Any, Callable

import httpx
import pytest

from plaidly import (
    Merchant,
    PaymentMethodInfo,
    PaymentSession,
    PlaidlyClient,
    PlaidlyError,
    Rate,
)

BASE_URL = "https://api.test.plaidly.io"

SESSION_BODY: dict[str, Any] = {
    "session_id": "ps_abc123",
    "merchant_id": "m_1",
    "expected_amount": 100.0,
    "received_amount": 0.0,
    "address": "0xdeadbeef",
    "status": "pending",
    "metadata": {"order_id": "42"},
    "expires_at": "2026-01-01T00:15:00Z",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "demo": False,
    "currency": "USDC",
    "payment_url": "https://pay.plaidly.io/ps_abc123",
    "qr_data": "solana:0xdeadbeef?amount=100",
    "explorer_url": "https://explorer/0xdeadbeef",
    "paymentMethod": {
        "methodID": 0,
        "chain": "solana",
        "token": "USDC",
        "network": "mainnet",
    },
}


def make_client(
    handler: Callable[[httpx.Request], httpx.Response],
) -> PlaidlyClient:
    """Build a PlaidlyClient whose HTTP layer is backed by a MockTransport."""
    client = PlaidlyClient(api_key="pk_test_key", base_url=BASE_URL)
    headers = client._http.headers
    client._http.close()
    client._http = httpx.Client(
        base_url=BASE_URL,
        headers=headers,
        transport=httpx.MockTransport(handler),
    )
    client.payment_sessions._http = client._http
    client.merchants._http = client._http
    return client


def json_response(status: int, body: Any) -> httpx.Response:
    return httpx.Response(status, content=json.dumps(body).encode(), headers={
        "Content-Type": "application/json",
    })


def test_create_payment_session() -> None:
    captured: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["url"] = str(request.url)
        captured["body"] = json.loads(request.content)
        captured["api_key"] = request.headers.get("X-API-Key")
        return json_response(201, SESSION_BODY)

    with make_client(handler) as client:
        session = client.payment_sessions.create(
            amount=100.0,
            chain="solana",
            token="USDC",
            metadata={"order_id": "42"},
        )

    assert captured["method"] == "POST"
    assert captured["url"].endswith("/v1/payment_sessions")
    assert captured["api_key"] == "pk_test_key"
    assert captured["body"]["amount"] == 100.0
    assert captured["body"]["expires_in"] == "15m"
    assert captured["body"]["paymentMethod"] == {
        "methodID": 0,
        "chain": "solana",
        "token": "USDC",
        "network": "mainnet",
    }
    assert isinstance(session, PaymentSession)
    assert session.session_id == "ps_abc123"
    assert session.payment_method is not None
    assert session.payment_method.method_id == 0
    assert session.payment_method.chain == "solana"
    assert session.metadata == {"order_id": "42"}
    assert session.is_paid is False


def test_get_payment_session() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/payment_sessions/ps_abc123"
        body = dict(SESSION_BODY, status="completed")
        return json_response(200, body)

    with make_client(handler) as client:
        session = client.payment_sessions.get("ps_abc123")

    assert session.status == "completed"
    assert session.is_paid is True


def test_create_demo_session() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/payment_sessions/demo"
        assert json.loads(request.content) == {"chain": "ethereum", "amount": 5.0}
        return json_response(201, dict(SESSION_BODY, demo=True))

    with make_client(handler) as client:
        session = client.payment_sessions.create_demo(chain="ethereum", amount=5.0)

    assert session.demo is True


def test_simulate_session() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/payment_sessions/ps_abc123/simulate"
        return json_response(200, dict(SESSION_BODY, status="completed"))

    with make_client(handler) as client:
        session = client.payment_sessions.simulate("ps_abc123")

    assert session.is_paid is True


def test_payment_methods() -> None:
    body = [
        {
            "chain": "solana",
            "network": "mainnet",
            "token": "USDC",
            "display_name": "USD Coin on Solana",
            "decimals": 6,
            "kind": "spl",
            "min_amount": 0.01,
        },
        {
            "chain": "ethereum",
            "network": "mainnet",
            "token": "ETH",
            "display_name": "Ethereum",
            "decimals": 18,
            "kind": "native",
        },
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/payment_methods"
        return json_response(200, body)

    with make_client(handler) as client:
        methods = client.payment_methods()

    assert len(methods) == 2
    assert all(isinstance(m, PaymentMethodInfo) for m in methods)
    assert methods[0].kind == "spl"
    assert methods[0].min_amount == 0.01
    assert methods[1].min_amount is None


def test_rates() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/rates"
        assert request.url.params.get("symbols") == "ETH,SOL"
        return json_response(
            200,
            [
                {"symbol": "ETH", "usd": 3000.0, "updated_at": "2026-01-01T00:00:00Z"},
                {"symbol": "SOL", "usd": 150.0, "updated_at": "2026-01-01T00:00:00Z"},
            ],
        )

    with make_client(handler) as client:
        rates = client.rates(symbols=["ETH", "SOL"])

    assert [r.symbol for r in rates] == ["ETH", "SOL"]
    assert isinstance(rates[0], Rate)
    assert rates[0].usd == 3000.0


def test_faucets() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/sandbox/faucets"
        return json_response(
            200, {"solana:testnet": "https://faucet.solana.com"}
        )

    with make_client(handler) as client:
        faucets = client.faucets()

    assert faucets == {"solana:testnet": "https://faucet.solana.com"}


def test_register_merchant() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/merchants"
        assert json.loads(request.content) == {
            "name": "Acme",
            "webhook_url": "https://acme.test/hook",
        }
        return json_response(
            201,
            {
                "id": "m_1",
                "name": "Acme",
                "created_at": "2026-01-01T00:00:00Z",
                "api_key": "pk_live_xyz",
                "webhook_secret": "whsec_abc",
                "webhook_url": "https://acme.test/hook",
                "rate_limit_per_minute": 60,
            },
        )

    with make_client(handler) as client:
        merchant = client.merchants.register(
            name="Acme", webhook_url="https://acme.test/hook"
        )

    assert isinstance(merchant, Merchant)
    assert merchant.api_key == "pk_live_xyz"
    assert merchant.webhook_secret == "whsec_abc"
    assert merchant.rate_limit_per_minute == 60


def test_get_me() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/me"
        return json_response(
            200,
            {"id": "m_1", "name": "Acme", "created_at": "2026-01-01T00:00:00Z"},
        )

    with make_client(handler) as client:
        merchant = client.merchants.me()

    assert merchant.id == "m_1"
    assert merchant.api_key is None


def test_error_mapping_with_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(400, {"code": 4001, "message": "invalid chain"})

    with make_client(handler) as client:
        with pytest.raises(PlaidlyError) as exc_info:
            client.payment_sessions.get("ps_missing")

    err = exc_info.value
    assert err.status == 400
    assert err.code == 4001
    assert err.message == "invalid chain"
    assert "invalid chain" in str(err)


def test_error_mapping_non_json_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, text="bad gateway")

    client = PlaidlyClient(api_key="pk_test_key", base_url=BASE_URL)
    headers = client._http.headers
    client._http.close()
    client._http = httpx.Client(
        base_url=BASE_URL,
        headers=headers,
        transport=httpx.MockTransport(handler),
    )
    client.payment_sessions._http = client._http

    with client:
        with pytest.raises(PlaidlyError) as exc_info:
            client.payment_sessions.get("ps_x")

    assert exc_info.value.status == 502
    assert exc_info.value.code is None


def test_retry_then_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("plaidly.client.time.sleep", lambda _: None)
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return json_response(503, {"code": 5000, "message": "unavailable"})
        return json_response(200, SESSION_BODY)

    with make_client(handler) as client:
        session = client.payment_sessions.get("ps_abc123")

    assert calls["n"] == 3
    assert session.session_id == "ps_abc123"


def test_missing_api_key_raises() -> None:
    with pytest.raises(ValueError):
        PlaidlyClient(api_key="")
