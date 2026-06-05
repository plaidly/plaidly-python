"""Typed data models mirroring the Plaidly API contract.

All field names match the JSON wire format (snake_case) exactly, so a model
can be built straight from a decoded response body via ``Model.from_dict``.
Unknown fields are ignored so additive API changes never break the SDK.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Optional, TypeVar, Type

T = TypeVar("T")


def _filtered(cls: Type[T], data: dict[str, Any]) -> dict[str, Any]:
    known = {f.name for f in fields(cls)}
    return {k: v for k, v in data.items() if k in known}


@dataclass(frozen=True)
class PaymentMethod:
    """A chain/token/network selector on a payment session.

    ``method_id`` maps to the wire field ``methodID`` (0 = crypto, 1 = fiat).
    """

    method_id: int
    chain: str
    token: str
    network: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaymentMethod":
        return cls(
            method_id=int(data.get("methodID", 0)),
            chain=str(data.get("chain", "")),
            token=str(data.get("token", "")),
            network=str(data.get("network", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "methodID": self.method_id,
            "chain": self.chain,
            "token": self.token,
            "network": self.network,
        }


@dataclass(frozen=True)
class PaymentSession:
    """A payment session returned by the Plaidly API.

    Statuses progress ``pending -> partial_paid -> paid -> finalizing ->
    confirmed -> completed`` with terminal failures ``expired`` and ``failed``.
    Treat ``completed`` or ``confirmed`` as success.
    """

    session_id: str
    merchant_id: str
    expected_amount: float
    received_amount: float
    address: str
    status: str
    metadata: dict[str, Any]
    expires_at: str
    created_at: str
    updated_at: str
    demo: bool
    payment_method: Optional[PaymentMethod] = None
    currency: Optional[str] = None
    payment_url: Optional[str] = None
    qr_data: Optional[str] = None
    explorer_url: Optional[str] = None
    completed_at: Optional[str] = None

    @property
    def is_paid(self) -> bool:
        """``True`` when the session reached a terminal success state."""
        return self.status in ("completed", "confirmed")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaymentSession":
        pm = data.get("paymentMethod")
        return cls(
            session_id=str(data.get("session_id", "")),
            merchant_id=str(data.get("merchant_id", "")),
            expected_amount=float(data.get("expected_amount", 0) or 0),
            received_amount=float(data.get("received_amount", 0) or 0),
            address=str(data.get("address", "")),
            status=str(data.get("status", "")),
            metadata=dict(data.get("metadata") or {}),
            expires_at=str(data.get("expires_at", "")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
            demo=bool(data.get("demo", False)),
            payment_method=PaymentMethod.from_dict(pm) if isinstance(pm, dict) else None,
            currency=data.get("currency"),
            payment_url=data.get("payment_url"),
            qr_data=data.get("qr_data"),
            explorer_url=data.get("explorer_url"),
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True)
class PaymentMethodInfo:
    """An enabled chain/token combination from ``GET /v1/payment_methods``."""

    chain: str
    network: str
    token: str
    display_name: str
    decimals: int
    kind: str
    min_amount: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaymentMethodInfo":
        return cls(
            chain=str(data.get("chain", "")),
            network=str(data.get("network", "")),
            token=str(data.get("token", "")),
            display_name=str(data.get("display_name", "")),
            decimals=int(data.get("decimals", 0)),
            kind=str(data.get("kind", "")),
            min_amount=(
                float(data["min_amount"]) if data.get("min_amount") is not None else None
            ),
        )


@dataclass(frozen=True)
class Rate:
    """A USD spot rate from ``GET /v1/rates``."""

    symbol: str
    usd: float
    updated_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Rate":
        return cls(
            symbol=str(data.get("symbol", "")),
            usd=float(data.get("usd", 0) or 0),
            updated_at=str(data.get("updated_at", "")),
        )


@dataclass(frozen=True)
class Merchant:
    """A merchant returned by ``POST /v1/merchants`` or ``GET /v1/me``.

    ``api_key`` and ``webhook_secret`` are only populated on registration.
    """

    id: str
    name: str
    created_at: str
    email: Optional[str] = None
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    rate_limit_per_minute: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Merchant":
        return cls(**_filtered(cls, data))
