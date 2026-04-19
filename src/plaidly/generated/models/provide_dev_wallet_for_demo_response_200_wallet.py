from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProvideDevWalletForDemoResponse200Wallet")


@_attrs_define
class ProvideDevWalletForDemoResponse200Wallet:
    """
    Attributes:
        public_key (str):
        private_key (str):
        explorer_url (str):
    """

    public_key: str
    private_key: str
    explorer_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        public_key = self.public_key

        private_key = self.private_key

        explorer_url = self.explorer_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "publicKey": public_key,
                "privateKey": private_key,
                "explorerURL": explorer_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public_key = d.pop("publicKey")

        private_key = d.pop("privateKey")

        explorer_url = d.pop("explorerURL")

        provide_dev_wallet_for_demo_response_200_wallet = cls(
            public_key=public_key,
            private_key=private_key,
            explorer_url=explorer_url,
        )

        provide_dev_wallet_for_demo_response_200_wallet.additional_properties = d
        return provide_dev_wallet_for_demo_response_200_wallet

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
