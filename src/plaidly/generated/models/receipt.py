import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Receipt")


@_attrs_define
class Receipt:
    """
    Attributes:
        id (str):
        session_id (str):
        merchant_id (str):
        issued_at (datetime.datetime):
        amount (float):
        currency (str):
    """

    id: str
    session_id: str
    merchant_id: str
    issued_at: datetime.datetime
    amount: float
    currency: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        session_id = self.session_id

        merchant_id = self.merchant_id

        issued_at = self.issued_at.isoformat()

        amount = self.amount

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "session_id": session_id,
                "merchant_id": merchant_id,
                "issued_at": issued_at,
                "amount": amount,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        session_id = d.pop("session_id")

        merchant_id = d.pop("merchant_id")

        issued_at = isoparse(d.pop("issued_at"))

        amount = d.pop("amount")

        currency = d.pop("currency")

        receipt = cls(
            id=id,
            session_id=session_id,
            merchant_id=merchant_id,
            issued_at=issued_at,
            amount=amount,
            currency=currency,
        )

        receipt.additional_properties = d
        return receipt

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
