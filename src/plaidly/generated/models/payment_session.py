from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_method import PaymentMethod
    from ..models.payment_session_metadata import PaymentSessionMetadata


T = TypeVar("T", bound="PaymentSession")


@_attrs_define
class PaymentSession:
    """
    Attributes:
        session_id (str):
        merchant_id (str):
        expected_amount (float):
        received_amount (float):
        address (str):
        status (str):
        metadata (PaymentSessionMetadata):
        expires_at (str):
        created_at (str):
        updated_at (str):
        demo (bool):
        payment_method (PaymentMethod):
        completed_at (Union[Unset, str]):
    """

    session_id: str
    merchant_id: str
    expected_amount: float
    received_amount: float
    address: str
    status: str
    metadata: "PaymentSessionMetadata"
    expires_at: str
    created_at: str
    updated_at: str
    demo: bool
    payment_method: "PaymentMethod"
    completed_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        merchant_id = self.merchant_id

        expected_amount = self.expected_amount

        received_amount = self.received_amount

        address = self.address

        status = self.status

        metadata = self.metadata.to_dict()

        expires_at = self.expires_at

        created_at = self.created_at

        updated_at = self.updated_at

        demo = self.demo

        payment_method = self.payment_method.to_dict()

        completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "merchant_id": merchant_id,
                "expected_amount": expected_amount,
                "received_amount": received_amount,
                "address": address,
                "status": status,
                "metadata": metadata,
                "expires_at": expires_at,
                "created_at": created_at,
                "updated_at": updated_at,
                "demo": demo,
                "paymentMethod": payment_method,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_method import PaymentMethod
        from ..models.payment_session_metadata import PaymentSessionMetadata

        d = dict(src_dict)
        session_id = d.pop("session_id")

        merchant_id = d.pop("merchant_id")

        expected_amount = d.pop("expected_amount")

        received_amount = d.pop("received_amount")

        address = d.pop("address")

        status = d.pop("status")

        metadata = PaymentSessionMetadata.from_dict(d.pop("metadata"))

        expires_at = d.pop("expires_at")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        demo = d.pop("demo")

        payment_method = PaymentMethod.from_dict(d.pop("paymentMethod"))

        completed_at = d.pop("completed_at", UNSET)

        payment_session = cls(
            session_id=session_id,
            merchant_id=merchant_id,
            expected_amount=expected_amount,
            received_amount=received_amount,
            address=address,
            status=status,
            metadata=metadata,
            expires_at=expires_at,
            created_at=created_at,
            updated_at=updated_at,
            demo=demo,
            payment_method=payment_method,
            completed_at=completed_at,
        )

        payment_session.additional_properties = d
        return payment_session

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
