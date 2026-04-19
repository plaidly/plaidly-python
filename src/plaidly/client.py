"""High-level Plaidly API client.

This module wraps the auto-generated low-level client in
:mod:`plaidly.generated` with retries, typed error handling, and a
friendly facade. Types come straight from the OpenAPI 3.1 spec — regenerate
with ``make generate``.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Optional, TypeVar

import httpx

from .generated.client import AuthenticatedClient
from .generated.api.merchants import get_me, register_merchant
from .generated.api.payment_sessions import (
    create_demo_payment_session,
    create_payment_session,
    fulfill_demo_payment_session,
    get_payment_session,
)
from .generated.api.payouts import get_payout, request_payout
from .generated.api.wallets import create_wallet, get_wallet, list_wallets
from .generated.api.transactions import list_transactions
from .generated.models import (
    CreatePaymentSessionRequest,
    CreateWalletRequest,
    Merchant,
    PaymentMethod,
    PaymentSession,
    Payout,
    RegisterMerchantRequest,
    RequestPayoutRequest,
    Transaction,
    Wallet,
)
from .generated.types import Response

T = TypeVar("T")


class PlaidlyError(Exception):
    """Raised when the Plaidly API returns a non-2xx response."""

    def __init__(self, message: str, status_code: int, code: str = "UNKNOWN_ERROR") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code


def _call_with_retries(fn: Callable[[], Response[T]]) -> Response[T]:
    """Execute a generated sync_detailed call with retries on 5xx / network errors."""
    last_exc: Optional[BaseException] = None
    for attempt in range(3):
        try:
            resp = fn()
            if resp.status_code >= 500 and attempt < 2:
                time.sleep(2**attempt * 0.5)
                continue
            return resp
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            last_exc = exc
            if attempt < 2:
                time.sleep(2**attempt * 0.5)
    assert last_exc is not None
    raise last_exc


def _unwrap(resp: Response[T]) -> T:
    """Return resp.parsed on 2xx; raise PlaidlyError on non-2xx."""
    if 200 <= resp.status_code < 300:
        if resp.parsed is None:
            # Should not happen for JSON endpoints documented as returning a body.
            raise PlaidlyError(
                f"empty response body (status {resp.status_code})",
                resp.status_code,
                "EMPTY_BODY",
            )
        return resp.parsed
    # Non-2xx — try to extract error details.
    message = f"HTTP {resp.status_code}"
    code = "UNKNOWN_ERROR"
    try:
        import json

        body = json.loads(resp.content.decode() if resp.content else "{}")
        if isinstance(body, dict):
            if isinstance(body.get("message"), str):
                message = body["message"]
            if isinstance(body.get("code"), str):
                code = body["code"]
    except (ValueError, UnicodeDecodeError):
        pass
    raise PlaidlyError(message, resp.status_code, code)


class PlaidlyClient:
    """Synchronous Plaidly API client.

    Args:
        api_key: Your Plaidly API key (sent as ``X-API-Key``).
        base_url: Override the default API base URL.
        timeout: HTTP request timeout in seconds (default 30).

    Example::

        client = PlaidlyClient(api_key="pk_live_...")
        session = client.payment_sessions.create(
            CreatePaymentSessionRequest(
                amount=100.0, expires_in="15m",
                payment_method=PaymentMethod(method_id=0, chain="solana",
                                             token="USDC", network="mainnet"),
            ),
        )
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.plaidly.io",
        timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._generated = AuthenticatedClient(
            base_url=base_url.rstrip("/"),
            token=api_key,
            prefix="",
            auth_header_name="X-API-Key",
            timeout=httpx.Timeout(timeout),
        )
        self.merchants = _MerchantsAPI(self._generated)
        self.payment_sessions = _PaymentSessionsAPI(self._generated)
        self.payouts = _PayoutsAPI(self._generated)
        self.wallets = _WalletsAPI(self._generated)

    @property
    def raw(self) -> AuthenticatedClient:
        """Return the underlying generated client (escape hatch)."""
        return self._generated

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._generated.get_httpx_client().close()

    def __enter__(self) -> "PlaidlyClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


class _MerchantsAPI:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def register(self, body: RegisterMerchantRequest) -> Merchant:
        resp = _call_with_retries(
            lambda: register_merchant.sync_detailed(client=self._client, body=body)
        )
        return _unwrap(resp)

    def me(self) -> Merchant:
        resp = _call_with_retries(lambda: get_me.sync_detailed(client=self._client))
        return _unwrap(resp)


class _PaymentSessionsAPI:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def create(self, body: CreatePaymentSessionRequest) -> PaymentSession:
        resp = _call_with_retries(
            lambda: create_payment_session.sync_detailed(client=self._client, body=body)
        )
        return _unwrap(resp)

    def create_demo(self) -> PaymentSession:
        resp = _call_with_retries(
            lambda: create_demo_payment_session.sync_detailed(client=self._client)
        )
        return _unwrap(resp)

    def get(self, session_id: str) -> PaymentSession:
        resp = _call_with_retries(
            lambda: get_payment_session.sync_detailed(client=self._client, session_id=session_id)
        )
        return _unwrap(resp)

    def fulfill_demo(self, session_id: str) -> None:
        resp = _call_with_retries(
            lambda: fulfill_demo_payment_session.sync_detailed(
                client=self._client, session_id=session_id
            )
        )
        if not (200 <= resp.status_code < 300):
            _unwrap(resp)  # raises PlaidlyError

    def receipt_pdf(self, session_id: str) -> bytes:
        """Fetch the PDF receipt for a completed session.

        The PDF endpoint is not covered by the generated client (it returns
        application/pdf, not JSON), so this wrapper issues the HTTP call
        directly via the underlying httpx.Client.
        """
        httpx_client = self._client.get_httpx_client()
        last_exc: Optional[BaseException] = None
        for attempt in range(3):
            try:
                resp = httpx_client.request(
                    "GET", f"/v1/payment_sessions/{session_id}/receipt"
                )
                if resp.status_code >= 500 and attempt < 2:
                    time.sleep(2**attempt * 0.5)
                    continue
                if 200 <= resp.status_code < 300:
                    return resp.content
                raise PlaidlyError(
                    f"HTTP {resp.status_code}", resp.status_code, "RECEIPT_FETCH_FAILED"
                )
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                if attempt < 2:
                    time.sleep(2**attempt * 0.5)
        assert last_exc is not None
        raise last_exc


class _PayoutsAPI:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def request(self, body: RequestPayoutRequest) -> Payout:
        resp = _call_with_retries(
            lambda: request_payout.sync_detailed(client=self._client, body=body)
        )
        return _unwrap(resp)

    def get(self, payout_id: str) -> Payout:
        resp = _call_with_retries(
            lambda: get_payout.sync_detailed(client=self._client, payout_id=payout_id)
        )
        return _unwrap(resp)


class _WalletsAPI:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def create(self, body: CreateWalletRequest) -> Wallet:
        resp = _call_with_retries(
            lambda: create_wallet.sync_detailed(client=self._client, body=body)
        )
        return _unwrap(resp)

    def list(self) -> list[Wallet]:
        resp = _call_with_retries(lambda: list_wallets.sync_detailed(client=self._client))
        return _unwrap(resp)

    def get(self, wallet_id: str) -> Wallet:
        resp = _call_with_retries(
            lambda: get_wallet.sync_detailed(client=self._client, wallet_id=wallet_id)
        )
        return _unwrap(resp)

    def transactions(self, wallet_id: str) -> list[Transaction]:
        resp = _call_with_retries(
            lambda: list_transactions.sync_detailed(client=self._client, wallet_id=wallet_id)
        )
        return _unwrap(resp)


__all__ = [
    "PlaidlyClient",
    "PlaidlyError",
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
