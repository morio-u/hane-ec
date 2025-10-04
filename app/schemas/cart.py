from pydantic import BaseModel, conint, Field, field_validator
from fastapi import Form


class SkuInfo(BaseModel):
    sku_id: int = Field(...)

    @field_validator("sku_id", mode="before")
    @classmethod
    def check_sku_id_is_int(cls, v):
        if not isinstance(v, int):
            raise TypeError("SKU ID must be an integer")
        return v


class QuantityInfo(BaseModel):
    quantity: conint(gt=0, le=5) = Field(
        ..., description="Quantity must be between 1 and 5"
    )


class UpdateCartForm(QuantityInfo):

    @classmethod
    def as_form(
        cls,
        quantity: int = Form(...),
    ):
        return cls(
            quantity=quantity,
        )


class AddToCartForm(SkuInfo, QuantityInfo):

    @classmethod
    def as_form(
        cls,
        sku_id: int = Form(...),
        quantity: int = Form(...),
    ):
        return cls(
            sku_id=sku_id,
            quantity=quantity,
        )
