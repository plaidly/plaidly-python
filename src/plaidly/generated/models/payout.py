from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Payout")


@_attrs_define
class Payout:
    """
    Attributes:
        id (str):
        merchant_id (str):
        destination_address (str):
        amount (float):
        token_symbol (str):
        network (str):
        status (str):
        requested_at (str):
        tx_hash (Union[Unset, str]):
        sent_at (Union[Unset, str]):
    """

    id: str
    merchant_id: str
    destination_address: str
    amount: float
    token_symbol: str
    network: str
    status: str
    requested_at: str
    tx_hash: Union[Unset, str] = UNSET
    sent_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        merchant_id = self.merchant_id

        destination_address = self.destination_address

        amount = self.amount

        token_symbol = self.token_symbol

        network = self.network

        status = self.status

        requested_at = self.requested_at

        tx_hash = self.tx_hash

        sent_at = self.sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "merchant_id": merchant_id,
                "destination_address": destination_address,
                "amount": amount,
                "token_symbol": token_symbol,
                "network": network,
                "status": status,
                "requested_at": requested_at,
            }
        )
        if tx_hash is not UNSET:
            field_dict["tx_hash"] = tx_hash
        if sent_at is not UNSET:
            field_dict["sent_at"] = sent_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        merchant_id = d.pop("merchant_id")

        destination_address = d.pop("destination_address")

        amount = d.pop("amount")

        token_symbol = d.pop("token_symbol")

        network = d.pop("network")

        status = d.pop("status")

        requested_at = d.pop("requested_at")

        tx_hash = d.pop("tx_hash", UNSET)

        sent_at = d.pop("sent_at", UNSET)

        payout = cls(
            id=id,
            merchant_id=merchant_id,
            destination_address=destination_address,
            amount=amount,
            token_symbol=token_symbol,
            network=network,
            status=status,
            requested_at=requested_at,
            tx_hash=tx_hash,
            sent_at=sent_at,
        )

        payout.additional_properties = d
        return payout

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
