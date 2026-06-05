"""Plaidly API client."""

from __future__ import annotations

import time
from typing import Any, Optional

import httpx

from .errors import PlaidlyError
from .models import (
    Merchant,
    PaymentMethod,
    PaymentMethodInfo,
    PaymentSession,
    Rate,
)

_RETRY_STATUS = {500, 502, 503, 504}


def _request(http: httpx.Client, method: str, path: str, **kwargs: Any) -> httpx.Response:
    """Execute an HTTP request with up to 3 attempts on transient failures.

    Retries on connection/timeout errors and 5xx responses with exponential
    backoff. The final response is returned regardless of status; callers map
    non-2xx responses to :class:`PlaidlyError` via :func:`_unwrap`.
    """
    last_exc: Optional[Exception] = None
    for attempt in range(3):
        try:
            resp = http.request(method, path, **kwargs)
            if resp.status_code in _RETRY_STATUS and attempt < 2:
                time.sleep(2**attempt * 0.5)
                continue
            return resp
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            last_exc = e
            if attempt < 2:
                time.sleep(2**attempt * 0.5)
    raise PlaidlyError(
        f"network error after retries: {last_exc}",
        status=0,
    )


def _unwrap(resp: httpx.Response) -> Any:
    """Raise :class:`PlaidlyError` on non-2xx, else return the decoded JSON body."""
    if resp.status_code >= 400:
        raise PlaidlyError.from_response(resp)
    if not resp.content:
        return None
    return resp.json()


class PlaidlyClient:
    """Synchronous Plaidly API client.

    Args:
        api_key: Your Plaidly API key, sent as the ``X-API-Key`` header.
        base_url: Override the default API base URL.
        timeout: HTTP request timeout in seconds (default: 30).

    Example::

        client = PlaidlyClient(api_key="pk_live_...")
        session = client.payment_sessions.create(
            amount=100.00,
            chain="solana",
            token="USDC",
        )
        print(session.address)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.plaidly.io",
        timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": api_key,
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
        self.payment_sessions = PaymentSessionsAPI(self._http)
        self.merchants = MerchantsAPI(self._http)

    def payment_methods(self) -> list[PaymentMethodInfo]:
        """List enabled payment methods (chain/token combinations)."""
        body = _unwrap(_request(self._http, "GET", "/v1/payment_methods"))
        return [PaymentMethodInfo.from_dict(m) for m in (body or [])]

    def rates(self, symbols: Optional[list[str]] = None) -> list[Rate]:
        """Get USD spot rates for supported assets.

        Args:
            symbols: Optional list of symbols (e.g. ``["ETH", "SOL"]``).
                Omit for all rates. Stablecoins are fixed at ``1.0``.
        """
        params: dict[str, str] = {}
        if symbols:
            params["symbols"] = ",".join(symbols)
        body = _unwrap(_request(self._http, "GET", "/v1/rates", params=params))
        return [Rate.from_dict(r) for r in (body or [])]

    def faucets(self) -> dict[str, str]:
        """List testnet faucet URLs keyed by ``chain:network``."""
        body = _unwrap(_request(self._http, "GET", "/v1/sandbox/faucets"))
        return dict(body or {})

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> "PlaidlyClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


class PaymentSessionsAPI:
    """Operations on payment sessions."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create(
        self,
        amount: float,
        chain: str,
        token: str,
        network: str = "mainnet",
        expires_in: str = "15m",
        method_id: int = 0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> PaymentSession:
        """Create a new payment session.

        Args:
            amount: Expected amount to be paid.
            chain: Blockchain name (e.g. ``"solana"``, ``"ethereum"``).
            token: Token symbol (e.g. ``"USDC"``, ``"ETH"``).
            network: Network name, ``"mainnet"`` or ``"testnet"``.
            expires_in: Duration until the session expires (e.g. ``"15m"``).
            method_id: ``0`` = crypto, ``1`` = fiat.
            metadata: Arbitrary key-value pairs attached to the session.
        """
        payload: dict[str, Any] = {
            "amount": amount,
            "expires_in": expires_in,
            "paymentMethod": PaymentMethod(
                method_id=method_id, chain=chain, token=token, network=network
            ).to_dict(),
        }
        if metadata is not None:
            payload["metadata"] = metadata
        body = _unwrap(
            _request(self._http, "POST", "/v1/payment_sessions", json=payload)
        )
        return PaymentSession.from_dict(body)

    def get(self, session_id: str) -> PaymentSession:
        """Fetch a payment session by ID (public — used for checkout polling)."""
        body = _unwrap(
            _request(self._http, "GET", f"/v1/payment_sessions/{session_id}")
        )
        return PaymentSession.from_dict(body)

    def create_demo(
        self,
        chain: Optional[str] = None,
        token: Optional[str] = None,
        network: Optional[str] = None,
        amount: Optional[float] = None,
    ) -> PaymentSession:
        """Create a public demo payment session.

        All arguments are optional; the API picks sensible defaults when omitted.
        """
        payload: dict[str, Any] = {}
        if chain is not None:
            payload["chain"] = chain
        if token is not None:
            payload["token"] = token
        if network is not None:
            payload["network"] = network
        if amount is not None:
            payload["amount"] = amount
        body = _unwrap(
            _request(self._http, "POST", "/v1/payment_sessions/demo", json=payload)
        )
        return PaymentSession.from_dict(body)

    def simulate(self, session_id: str) -> PaymentSession:
        """Instantly complete a demo/sandbox session's payment.

        Only valid for demo or sandbox sessions in a pending state.
        """
        body = _unwrap(
            _request(
                self._http,
                "POST",
                f"/v1/payment_sessions/{session_id}/simulate",
            )
        )
        return PaymentSession.from_dict(body)


class MerchantsAPI:
    """Operations on merchants."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def register(
        self,
        name: str,
        webhook_url: Optional[str] = None,
    ) -> Merchant:
        """Register a new merchant and receive an API key.

        Args:
            name: Merchant display name.
            webhook_url: Optional URL to receive webhook events.

        Returns:
            The created merchant, including ``api_key`` and ``webhook_secret``.
        """
        payload: dict[str, Any] = {"name": name}
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        body = _unwrap(_request(self._http, "POST", "/v1/merchants", json=payload))
        return Merchant.from_dict(body)

    def me(self) -> Merchant:
        """Return the authenticated merchant's profile."""
        body = _unwrap(_request(self._http, "GET", "/v1/me"))
        return Merchant.from_dict(body)
