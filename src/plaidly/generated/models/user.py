from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """User model containing essential user details

    Attributes:
        id (str): User's ID
        personal_wallet_address (str): The user's personal wallet address
        created_wallet_address (str): The address of the wallet created for the user
        last_login_at (str): The last login timestamp in Unix format Example: 1672531200.
    """

    id: str
    personal_wallet_address: str
    created_wallet_address: str
    last_login_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        personal_wallet_address = self.personal_wallet_address

        created_wallet_address = self.created_wallet_address

        last_login_at = self.last_login_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "personal_wallet_address": personal_wallet_address,
                "created_wallet_address": created_wallet_address,
                "last_login_at": last_login_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        personal_wallet_address = d.pop("personal_wallet_address")

        created_wallet_address = d.pop("created_wallet_address")

        last_login_at = d.pop("last_login_at")

        user = cls(
            id=id,
            personal_wallet_address=personal_wallet_address,
            created_wallet_address=created_wallet_address,
            last_login_at=last_login_at,
        )

        user.additional_properties = d
        return user

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
