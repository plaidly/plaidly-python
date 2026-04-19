from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provide_dev_wallet_for_demo_response_200_wallet import (
        ProvideDevWalletForDemoResponse200Wallet,
    )


T = TypeVar("T", bound="ProvideDevWalletForDemoResponse200")


@_attrs_define
class ProvideDevWalletForDemoResponse200:
    """
    Attributes:
        wallet (Union[Unset, ProvideDevWalletForDemoResponse200Wallet]):
    """

    wallet: Union[Unset, "ProvideDevWalletForDemoResponse200Wallet"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        wallet: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wallet, Unset):
            wallet = self.wallet.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if wallet is not UNSET:
            field_dict["wallet"] = wallet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provide_dev_wallet_for_demo_response_200_wallet import (
            ProvideDevWalletForDemoResponse200Wallet,
        )

        d = dict(src_dict)
        _wallet = d.pop("wallet", UNSET)
        wallet: Union[Unset, ProvideDevWalletForDemoResponse200Wallet]
        if isinstance(_wallet, Unset):
            wallet = UNSET
        else:
            wallet = ProvideDevWalletForDemoResponse200Wallet.from_dict(_wallet)

        provide_dev_wallet_for_demo_response_200 = cls(
            wallet=wallet,
        )

        provide_dev_wallet_for_demo_response_200.additional_properties = d
        return provide_dev_wallet_for_demo_response_200

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
