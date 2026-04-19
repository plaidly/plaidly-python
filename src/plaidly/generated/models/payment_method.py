from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.payment_method_method_id import PaymentMethodMethodID

T = TypeVar("T", bound="PaymentMethod")


@_attrs_define
class PaymentMethod:
    """
    Attributes:
        method_id (PaymentMethodMethodID): 0 = crypto, 1 = fiat
        chain (str):
        token (str):
        network (str):
    """

    method_id: PaymentMethodMethodID
    chain: str
    token: str
    network: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method_id = self.method_id.value

        chain = self.chain

        token = self.token

        network = self.network

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "methodID": method_id,
                "chain": chain,
                "token": token,
                "network": network,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method_id = PaymentMethodMethodID(d.pop("methodID"))

        chain = d.pop("chain")

        token = d.pop("token")

        network = d.pop("network")

        payment_method = cls(
            method_id=method_id,
            chain=chain,
            token=token,
            network=network,
        )

        payment_method.additional_properties = d
        return payment_method

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
