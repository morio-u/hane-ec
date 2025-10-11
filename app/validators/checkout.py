from typing import List
from sqlalchemy.orm import Session
from app.schemas.checkout import CheckoutConfirmForm


def validate_checkout_confirm(form: CheckoutConfirmForm, db: Session) -> List[str]:
    """
    Validate if the SKU exists and the quantity is acceptable for adding to the cart.

    Args:
        sku_id (int): The ID of the SKU to validate.
        quantity (int): The requested quantity to add.
        db (Session): The database session for querying SKU information.

    Returns:
        List[str]: A list of error messages. Empty if no errors.

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
    """
    errors = []

    # Check required items
    required_fields = {
        "last_name": form.shipping_last_name,
        "first_name": form.shipping_first_name,
        "address_line1": form.shipping_address_line1,
        "city": form.shipping_city,
        "state": form.shipping_state,
        "zip_code": form.shipping_zip,
        "phone_number": form.shipping_phone_number,
        "method": form.shipping_method,
        "payment_method": form.payment_method,
        "card_number": form.card_number,
        "card_name": form.card_name,
        "card_cvv": form.card_cvv,
    }

    for field_name, value in required_fields.items():
        if not value or value.strip() == "":
            errors.append(f"{field_name.replace('_', ' ').title()} is required.")

    # If there is an error in the required field check, return it.
    if errors:
        return errors

    return errors
