from decimal import Decimal
from pydantic import BaseModel, Field, condecimal, constr
from typing import Optional


class ShippingInfo(BaseModel):
    shipping_last_name: constr(min_length=1, max_length=50)
    shipping_first_name: constr(min_length=1, max_length=50)
    shipping_address_line1: constr(min_length=1, max_length=100)
    shipping_address_line2: Optional[constr(min_length=1, max_length=100)]
    shipping_city: constr(min_length=1, max_length=50)
    shipping_state: constr(min_length=1, max_length=50)
    shipping_zip: constr(regex=r"^\d{5}(-\d{4})?$")
    shipping_phone_number: constr(regex=r"^\+?[0-9\-]{7,15}$")
    shipping_method: constr(min_length=1, max_length=50)


class PaymentInfo(BaseModel):
    card_number: constr(regex=r"^\d{13,19}$")
    card_name: constr(in_length=1, max_length=50)
    card_cvv: constr(regex=r"^\d{3,4}$")

class CheckoutConfirmForm(ShippingInfo, PaymentInfo):
    payment_method: constr(min_length=1, max_length=50)