from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import UploadFile, File, Form


class SaveProductForm(BaseModel):
    id: int = Field(...)
    internal_part_number: str = Field(...)
    manufacturer_part_number: Optional[str] = Field(None)
    name: str = Field(...)
    brand_id: int = Field(...)
    department_id: int = Field(...)
    category_id: int = Field(...)
    subcategory_id: int = Field(...)
    purchase_type: int = Field(...)
    price_excluding_tax: Optional[float] = Field(None)
    cost_price: Optional[float] = Field(None)
    status: str = Field(...)
    description: Optional[str] = Field(None)
    image_files: Optional[List[UploadFile]] = File(None)

    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        internal_part_number: str = Form(...),
        manufacturer_part_number: Optional[str] = Form(None),
        name: str = Form(...),
        brand_id: int = Form(...),
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
        return cls(
            id=id,
            internal_part_number=internal_part_number,
            manufacturer_part_number=manufacturer_part_number,
            name=name,
            brand_id=brand_id,
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
