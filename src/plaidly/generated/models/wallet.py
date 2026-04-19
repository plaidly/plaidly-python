from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Wallet")


@_attrs_define
class Wallet:
    """
    Attributes:
        id (str):
        network (str):
        address (str):
        private_key_encrypted (str):
        type_ (str): session, cold, or hot
        created_at (str):
        assigned_session_id (Union[Unset, str]):
    """

    id: str
    network: str
    address: str
    private_key_encrypted: str
    type_: str
    created_at: str
    assigned_session_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        network = self.network

        address = self.address

        private_key_encrypted = self.private_key_encrypted

        type_ = self.type_

        created_at = self.created_at

        assigned_session_id = self.assigned_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "network": network,
                "address": address,
                "private_key_encrypted": private_key_encrypted,
                "type": type_,
                "created_at": created_at,
            }
        )
        if assigned_session_id is not UNSET:
            field_dict["assigned_session_id"] = assigned_session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        network = d.pop("network")

        address = d.pop("address")

        private_key_encrypted = d.pop("private_key_encrypted")

        type_ = d.pop("type")

        created_at = d.pop("created_at")

        assigned_session_id = d.pop("assigned_session_id", UNSET)

        wallet = cls(
            id=id,
            network=network,
            address=address,
            private_key_encrypted=private_key_encrypted,
            type_=type_,
            created_at=created_at,
            assigned_session_id=assigned_session_id,
        )

        wallet.additional_properties = d
        return wallet

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
