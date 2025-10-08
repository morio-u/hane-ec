from pydantic import BaseModel, conint, Field
from fastapi import Form


class AddToCartForm(BaseModel):
    sku_id: int = Field(...)
    quantity: int = Field(...)
    product_id: int = Field(...)

    @classmethod
    def as_form(
        cls,
        sku_id: int = Form(...),
        quantity: int = Form(...),
        product_id: int = Form(...),
    ) -> "AddToCartForm":
        return cls(
            sku_id=sku_id,
            quantity=quantity,
            product_id=product_id,
        )
