from pydantic import BaseModel, Field, constr
from typing import Optional
from fastapi import Form


class ShippingInfo(BaseModel):
    shipping_last_name: constr(min_length=1, max_length=50)
    shipping_first_name: constr(min_length=1, max_length=50)
    shipping_address_line1: constr(min_length=1, max_length=100)
    shipping_address_line2: Optional[constr(max_length=100)] = Field(default=None)
    shipping_city: constr(min_length=1, max_length=50)
    shipping_state: constr(min_length=1, max_length=50)
    shipping_zip: constr(pattern=r"^\d{5}(-\d{4})?$")
    shipping_phone_number: constr(pattern=r"^\+?[0-9\-]{7,15}$")
    shipping_method: constr(min_length=1, max_length=50)


class PaymentInfo(BaseModel):
    card_number: constr(pattern=r"^\d{13,19}$")
    card_name: constr(min_length=1, max_length=50)
    card_cvv: constr(pattern=r"^\d{3,4}$")


class CheckoutConfirmForm(ShippingInfo, PaymentInfo):
    payment_method: constr(min_length=1, max_length=50)

    @classmethod
    def as_form(
        cls,
        shipping_last_name: str = Form(...),
        shipping_first_name: str = Form(...),
        shipping_address_line1: str = Form(...),
        shipping_address_line2: Optional[str] = Form(""),
        shipping_city: str = Form(...),
        shipping_state: str = Form(...),
        shipping_zip: str = Form(...),
        shipping_phone_number: str = Form(...),
        shipping_method: str = Form(...),
        payment_method: str = Form(...),
        card_number: str = Form(...),
        card_name: str = Form(...),
        card_cvv: str = Form(...),
    ):
        return cls(
            shipping_last_name=shipping_last_name,
            shipping_first_name=shipping_first_name,
            shipping_address_line1=shipping_address_line1,
            shipping_address_line2=shipping_address_line2,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zip=shipping_zip,
            shipping_phone_number=shipping_phone_number,
            shipping_method=shipping_method,
            payment_method=payment_method,
            card_number=card_number,
            card_name=card_name,
            card_cvv=card_cvv,
        )


class CheckoutCompleteForm(ShippingInfo):
    payment_method: constr(min_length=1, max_length=50)

    @classmethod
    def as_form(
        cls,
        shipping_last_name: str = Form(...),
        shipping_first_name: str = Form(...),
        shipping_address_line1: str = Form(...),
        shipping_address_line2: Optional[str] = Form(""),
        shipping_city: str = Form(...),
        shipping_state: str = Form(...),
        shipping_zip: str = Form(...),
        shipping_phone_number: str = Form(...),
        shipping_method: str = Form(...),
        payment_method: str = Form(...),
    ):
        return cls(
            shipping_last_name=shipping_last_name,
            shipping_first_name=shipping_first_name,
            shipping_address_line1=shipping_address_line1,
            shipping_address_line2=shipping_address_line2,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zip=shipping_zip,
            shipping_phone_number=shipping_phone_number,
            shipping_method=shipping_method,
            payment_method=payment_method,
        )


# This temporary form model is used for Jinja2 templates until we switch to React.
class ShippingInfoTmp(BaseModel):
    shipping_last_name: Optional[str] = None
    shipping_first_name: Optional[str] = None
    shipping_address_line1: Optional[str] = None
    shipping_address_line2: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_zip: Optional[str] = None
    shipping_phone_number: Optional[str] = None
    shipping_method: Optional[str] = None


class PaymentInfoTmp(BaseModel):
    card_number: Optional[str] = None
    card_name: Optional[str] = None
    card_cvv: Optional[str] = None


class CheckoutConfirmFormTmp(ShippingInfoTmp, PaymentInfoTmp):
    payment_method: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        shipping_last_name: Optional[str] = Form(None),
        shipping_first_name: Optional[str] = Form(None),
        shipping_address_line1: Optional[str] = Form(None),
        shipping_address_line2: Optional[str] = Form(None),
        shipping_city: Optional[str] = Form(None),
        shipping_state: Optional[str] = Form(None),
        shipping_zip: Optional[str] = Form(None),
        shipping_phone_number: Optional[str] = Form(None),
        shipping_method: Optional[str] = Form(None),
        payment_method: Optional[str] = Form(None),
        card_number: Optional[str] = Form(None),
        card_name: Optional[str] = Form(None),
        card_cvv: Optional[str] = Form(None),
    ):
        return cls(
            shipping_last_name=shipping_last_name,
            shipping_first_name=shipping_first_name,
            shipping_address_line1=shipping_address_line1,
            shipping_address_line2=shipping_address_line2,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zip=shipping_zip,
            shipping_phone_number=shipping_phone_number,
            shipping_method=shipping_method,
            payment_method=payment_method,
            card_number=card_number,
            card_name=card_name,
            card_cvv=card_cvv,
        )


class CheckoutCompleteFormTmp(ShippingInfoTmp, PaymentInfoTmp):
    payment_method: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        shipping_last_name: Optional[str] = Form(None),
        shipping_first_name: Optional[str] = Form(None),
        shipping_address_line1: Optional[str] = Form(None),
        shipping_address_line2: Optional[str] = Form(None),
        shipping_city: Optional[str] = Form(None),
        shipping_state: Optional[str] = Form(None),
        shipping_zip: Optional[str] = Form(None),
        shipping_phone_number: Optional[str] = Form(None),
        shipping_method: Optional[str] = Form(None),
        payment_method: Optional[str] = Form(None),
        card_number: Optional[str] = Form(None),
        card_name: Optional[str] = Form(None),
        card_cvv: Optional[str] = Form(None),
    ):
        return cls(
            shipping_last_name=shipping_last_name,
            shipping_first_name=shipping_first_name,
            shipping_address_line1=shipping_address_line1,
            shipping_address_line2=shipping_address_line2,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zip=shipping_zip,
            shipping_phone_number=shipping_phone_number,
            shipping_method=shipping_method,
            payment_method=payment_method,
            card_number=card_number,
            card_name=card_name,
            card_cvv=card_cvv,
        )
