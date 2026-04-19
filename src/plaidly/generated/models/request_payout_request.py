from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RequestPayoutRequest")


@_attrs_define
class RequestPayoutRequest:
    """
    Attributes:
        destination_address (str): Blockchain address to send the payout to
        amount (float): Amount to pay out
        token_symbol (str): Token symbol (e.g. SOL, ETH)
        network (str): Blockchain network (e.g. solana, ethereum)
    """

    destination_address: str
    amount: float
    token_symbol: str
    network: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_address = self.destination_address

        amount = self.amount

        token_symbol = self.token_symbol

        network = self.network

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination_address": destination_address,
                "amount": amount,
                "token_symbol": token_symbol,
                "network": network,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination_address = d.pop("destination_address")

        amount = d.pop("amount")

        token_symbol = d.pop("token_symbol")

        network = d.pop("network")

        request_payout_request = cls(
            destination_address=destination_address,
            amount=amount,
            token_symbol=token_symbol,
            network=network,
        )

        request_payout_request.additional_properties = d
        return request_payout_request

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
