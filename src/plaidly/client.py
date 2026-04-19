"""Plaidly API client."""

from __future__ import annotations

import httpx
from typing import Any, Optional


class PlaidlyClient:
    """Synchronous Plaidly API client.

    Args:
        api_key: Your Plaidly API key (``X-API-Key`` header).
        base_url: Override the default API base URL.
        timeout: HTTP request timeout in seconds (default: 30).

    Example::

        client = PlaidlyClient(api_key="pk_live_...")
        session = client.sessions.create(
            amount="100.00",
            currency="USDC",
            chain="solana",
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
        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
        self.sessions = SessionsAPI(self._http)
        self.merchants = MerchantsAPI(self._http)
        self.payouts = PayoutsAPI(self._http)
        self.sandbox = SandboxAPI(self._http)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> "PlaidlyClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


class SessionsAPI:
    """Operations on payment sessions."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create(
        self,
        amount: str,
        currency: str,
        chain: str,
        network: str = "mainnet",
        callback_url: Optional[str] = None,
        metadata: Optional[dict[str, str]] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new payment session.

        Args:
            amount: Payment amount as a decimal string (e.g. ``"100.00"``).
            currency: Token symbol (e.g. ``"USDC"``, ``"ETH"``).
            chain: Blockchain name (e.g. ``"solana"``, ``"ethereum"``).
            network: Network name (default: ``"mainnet"``).
            callback_url: URL that Plaidly will POST webhook events to.
            metadata: Arbitrary key-value pairs attached to the session.
            idempotency_key: Optional idempotency key for safe retries.

        Returns:
            Session dict.
        """
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "chain": chain,
            "network": network,
        }
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if metadata is not None:
            payload["metadata"] = metadata
        if idempotency_key is not None:
            payload["idempotency_key"] = idempotency_key
        resp = self._http.post("/v1/sessions", json=payload)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def get(self, session_id: str) -> dict[str, Any]:
        """Fetch a session by ID.

        Args:
            session_id: Session identifier.

        Returns:
            Session dict.
        """
        resp = self._http.get(f"/v1/sessions/{session_id}")
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def list(self) -> dict[str, Any]:
        """List all sessions for the authenticated merchant.

        Returns:
            Dict with ``sessions`` list and ``total`` count.
        """
        resp = self._http.get("/v1/sessions")
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def simulate(self, session_id: str, tx_hash: Optional[str] = None) -> None:
        """Simulate a payment for a sandbox session.

        Args:
            session_id: Session identifier.
            tx_hash: Optional mock transaction hash.
        """
        payload: dict[str, Any] = {}
        if tx_hash is not None:
            payload["tx_hash"] = tx_hash
        resp = self._http.post(f"/v1/sessions/{session_id}/simulate", json=payload)
        resp.raise_for_status()


class MerchantsAPI:
    """Operations on merchants."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def register(
        self,
        name: str,
        email: str,
        webhook_url: Optional[str] = None,
        sandbox: bool = False,
    ) -> dict[str, Any]:
        """Register a new merchant.

        Args:
            name: Merchant display name.
            email: Contact email address.
            webhook_url: URL to receive webhook events.
            sandbox: When ``True``, creates a sandbox merchant.

        Returns:
            Merchant dict including the generated API key.
        """
        payload: dict[str, Any] = {"name": name, "email": email, "sandbox": sandbox}
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        resp = self._http.post("/v1/merchants", json=payload)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def me(self) -> dict[str, Any]:
        """Return the authenticated merchant's profile.

        Returns:
            Merchant dict.
        """
        resp = self._http.get("/v1/me")
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]


class PayoutsAPI:
    """Operations on payouts."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create(
        self,
        amount: str,
        currency: str,
        chain: str,
        address: str,
        network: str = "mainnet",
    ) -> dict[str, Any]:
        """Request a payout.

        Args:
            amount: Amount to pay out as a decimal string.
            currency: Token symbol.
            chain: Blockchain name.
            address: Destination wallet address.
            network: Network name (default: ``"mainnet"``).

        Returns:
            Payout dict.
        """
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "chain": chain,
            "network": network,
            "address": address,
        }
        resp = self._http.post("/v1/payouts", json=payload)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def get(self, payout_id: str) -> dict[str, Any]:
        """Fetch a payout by ID.

        Args:
            payout_id: Payout identifier.

        Returns:
            Payout dict.
        """
        resp = self._http.get(f"/v1/payouts/{payout_id}")
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]


class SandboxAPI:
    """Sandbox-only helpers."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def faucets(self) -> list[dict[str, Any]]:
        """Return available testnet faucets.

        Returns:
            List of faucet dicts with ``chain``, ``network``, ``url``, ``description``.
        """
        resp = self._http.get("/v1/sandbox/faucets")
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]
