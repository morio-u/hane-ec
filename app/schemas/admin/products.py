from decimal import Decimal
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator
from fastapi import UploadFile, File, Form


class SaveProductForm(BaseModel):
    id: Optional[Union[int, str]] = Field(None)
    internal_part_number: str = Field(...)
    manufacturer_part_number: Optional[str] = Field(None)
    name: str = Field(...)
    brand_id: int = Field(...)
    shipping_rule_id: Optional[int] = Field(None)
    department_id: int = Field(...)
    category_id: int = Field(...)
    subcategory_id: int = Field(...)
    purchase_type: int = Field(...)
    price_excluding_tax: Optional[Decimal] = Field(None)
    cost_price: Optional[Decimal] = Field(None)
    status: str = Field(...)
    description: Optional[str] = Field(None)

    @field_validator("id", mode="before")
    def empty_str_to_none(cls, v):
        if v in ("", None):
            return None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    @classmethod
    def as_form(
        cls,
        id: Optional[Union[int, str]] = Form(None),
        internal_part_number: str = Form(...),
        manufacturer_part_number: Optional[str] = Form(None),
        name: str = Form(...),
        brand_id: int = Form(...),
        shipping_rule_id: Optional[int] = Form(None),
        department_id: int = Form(...),
        category_id: int = Form(...),
        subcategory_id: int = Form(...),
        purchase_type: int = Form(...),
        price_excluding_tax: Optional[float] = Form(None),
        cost_price: Optional[float] = Form(None),
        status: str = Form(...),
        description: Optional[str] = Form(None),
        image_files: Optional[List[UploadFile]] = File(None),
    ) -> "SaveProductForm":
        return (
            cls(
                id=id,
                internal_part_number=internal_part_number,
                manufacturer_part_number=manufacturer_part_number,
                name=name,
                brand_id=brand_id,
                shipping_rule_id=shipping_rule_id,
                department_id=department_id,
                category_id=category_id,
                subcategory_id=subcategory_id,
                purchase_type=purchase_type,
                price_excluding_tax=price_excluding_tax,
                cost_price=cost_price,
                status=status,
                description=description,
            ),
            image_files,
        )


# This temporary form model is used for Jinja2 templates until we switch to React.
class SaveProductFormTmp(BaseModel):
    id: Optional[Union[int, str]] = None
    internal_part_number: Optional[str] = None
    manufacturer_part_number: Optional[str] = None
    name: Optional[str] = None
    brand_id: Optional[Union[int, str]] = None
    shipping_rule_id: Optional[Union[int, str]] = None
    department_id: Optional[Union[int, str]] = None
    category_id: Optional[Union[int, str]] = None
    subcategory_id: Optional[Union[int, str]] = None
    purchase_type: Optional[Union[int, str]] = None
    price_excluding_tax: Optional[Union[float, str]] = None
    cost_price: Optional[Union[float, str]] = None
    status: Optional[str] = None
    description: Optional[str] = None
    image_files: Optional[List[UploadFile]] = File(None)

    @field_validator("id", mode="before")
    def empty_str_to_none(cls, v):
        if v in ("", None):
            return None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    @classmethod
    def as_form(
        cls,
        id: Optional[Union[int, str]] = Form(None),
        internal_part_number: Optional[str] = Form(None),
        manufacturer_part_number: Optional[str] = Form(None),
        name: Optional[str] = Form(None),
        brand_id: Optional[Union[int, str]] = Form(None),
        shipping_rule_id: Optional[Union[int, str]] = Form(None),
        department_id: Optional[Union[int, str]] = Form(None),
        category_id: Optional[Union[int, str]] = Form(None),
        subcategory_id: Optional[Union[int, str]] = Form(None),
        purchase_type: Optional[Union[int, str]] = Form(None),
        price_excluding_tax: Optional[Union[float, str]] = Form(None),
        cost_price: Optional[Union[float, str]] = Form(None),
        status: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        image_files: Optional[List[UploadFile]] = File(None),
    ):
        return cls(
            id=id,
            internal_part_number=internal_part_number,
            manufacturer_part_number=manufacturer_part_number,
            name=name,
            brand_id=brand_id,
            shipping_rule_id=shipping_rule_id,
            department_id=department_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            purchase_type=purchase_type,
            price_excluding_tax=price_excluding_tax,
            cost_price=cost_price,
            status=status,
            description=description,
            image_files=image_files,
        )
