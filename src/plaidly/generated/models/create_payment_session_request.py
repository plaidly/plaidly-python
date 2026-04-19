from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_payment_session_request_metadata import (
        CreatePaymentSessionRequestMetadata,
    )
    from ..models.payment_method import PaymentMethod


T = TypeVar("T", bound="CreatePaymentSessionRequest")


@_attrs_define
class CreatePaymentSessionRequest:
    """
    Attributes:
        amount (float): Expected amount to be paid
        expires_in (str): Duration until session expires (e.g. 15m, 1h)
        payment_method (PaymentMethod):
        metadata (Union[Unset, CreatePaymentSessionRequestMetadata]): Optional key-value metadata (max 4KB)
    """

    amount: float
    expires_in: str
    payment_method: "PaymentMethod"
    metadata: Union[Unset, "CreatePaymentSessionRequestMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        expires_in = self.expires_in

        payment_method = self.payment_method.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "expires_in": expires_in,
                "paymentMethod": payment_method,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_payment_session_request_metadata import (
            CreatePaymentSessionRequestMetadata,
        )
        from ..models.payment_method import PaymentMethod

        d = dict(src_dict)
        amount = d.pop("amount")

        expires_in = d.pop("expires_in")

        payment_method = PaymentMethod.from_dict(d.pop("paymentMethod"))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CreatePaymentSessionRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreatePaymentSessionRequestMetadata.from_dict(_metadata)

        create_payment_session_request = cls(
            amount=amount,
            expires_in=expires_in,
            payment_method=payment_method,
            metadata=metadata,
        )

        create_payment_session_request.additional_properties = d
        return create_payment_session_request

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
