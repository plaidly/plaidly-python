from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Merchant")


@_attrs_define
class Merchant:
    """
    Attributes:
        id (str):
        name (str):
        api_key (str): API key for authenticating requests
        created_at (str):
        email (Union[Unset, str]):
        webhook_url (Union[Unset, str]):
        rate_limit_per_minute (Union[Unset, int]):
    """

    id: str
    name: str
    api_key: str
    created_at: str
    email: Union[Unset, str] = UNSET
    webhook_url: Union[Unset, str] = UNSET
    rate_limit_per_minute: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        api_key = self.api_key

        created_at = self.created_at

        email = self.email

        webhook_url = self.webhook_url

        rate_limit_per_minute = self.rate_limit_per_minute

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "api_key": api_key,
                "created_at": created_at,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if webhook_url is not UNSET:
            field_dict["webhook_url"] = webhook_url
        if rate_limit_per_minute is not UNSET:
            field_dict["rate_limit_per_minute"] = rate_limit_per_minute

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        api_key = d.pop("api_key")

        created_at = d.pop("created_at")

        email = d.pop("email", UNSET)

        webhook_url = d.pop("webhook_url", UNSET)

        rate_limit_per_minute = d.pop("rate_limit_per_minute", UNSET)

        merchant = cls(
            id=id,
            name=name,
            api_key=api_key,
            created_at=created_at,
            email=email,
            webhook_url=webhook_url,
            rate_limit_per_minute=rate_limit_per_minute,
        )

        merchant.additional_properties = d
        return merchant

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
