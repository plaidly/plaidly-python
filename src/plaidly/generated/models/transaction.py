from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """
    Attributes:
        id (str):
        tx_hash (str):
        session_id (str):
        network (str):
        token_symbol (str):
        amount (float):
        detected_at (str):
        confirmed (bool):
        from_address (Union[Unset, str]):
        to_address (Union[Unset, str]):
        block_number (Union[Unset, int]):
    """

    id: str
    tx_hash: str
    session_id: str
    network: str
    token_symbol: str
    amount: float
    detected_at: str
    confirmed: bool
    from_address: Union[Unset, str] = UNSET
    to_address: Union[Unset, str] = UNSET
    block_number: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tx_hash = self.tx_hash

        session_id = self.session_id

        network = self.network

        token_symbol = self.token_symbol

        amount = self.amount

        detected_at = self.detected_at

        confirmed = self.confirmed

        from_address = self.from_address

        to_address = self.to_address

        block_number = self.block_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tx_hash": tx_hash,
                "session_id": session_id,
                "network": network,
                "token_symbol": token_symbol,
                "amount": amount,
                "detected_at": detected_at,
                "confirmed": confirmed,
            }
        )
        if from_address is not UNSET:
            field_dict["from_address"] = from_address
        if to_address is not UNSET:
            field_dict["to_address"] = to_address
        if block_number is not UNSET:
            field_dict["block_number"] = block_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        tx_hash = d.pop("tx_hash")

        session_id = d.pop("session_id")

        network = d.pop("network")

        token_symbol = d.pop("token_symbol")

        amount = d.pop("amount")

        detected_at = d.pop("detected_at")

        confirmed = d.pop("confirmed")

        from_address = d.pop("from_address", UNSET)

        to_address = d.pop("to_address", UNSET)

        block_number = d.pop("block_number", UNSET)

        transaction = cls(
            id=id,
            tx_hash=tx_hash,
            session_id=session_id,
            network=network,
            token_symbol=token_symbol,
            amount=amount,
            detected_at=detected_at,
            confirmed=confirmed,
            from_address=from_address,
            to_address=to_address,
            block_number=block_number,
        )

        transaction.additional_properties = d
        return transaction

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
