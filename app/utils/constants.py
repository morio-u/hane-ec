import re
from decimal import Decimal
from typing import Optional
from app.models.sku import SkuStatusEnum


def get_skus_with_form(form_data: dict) -> Optional[dict[str, dict[str, str]]]:
    """
    Extracts SKU data from form input names and organizes it into a nested dictionary.

    Parameters:
        form_data (FormData): The form data containing key-value pairs from an HTML form.

    Returns:
        dict[str, dict[str, str]]:
            A nested dictionary mapping each SKU ID to its corresponding field values.
            Example:
                {
                    "1": {"color": "red", "size": "M"},
                    "2": {"color": "blue"}
                }
    """
    skus = {}
    # Retrieve all keys and values from the form
    for key, value in form_data.items():
        # Only process entries whose name starts with "sku_inp["
        if key.startswith("sku_inp["):
            # Extract the SKU ID and field name from the key
            match = re.match(r"sku_inp\[(\d+)\]\[(\w+)\]", key)
            if match:
                # Group individual SKU fields into a dictionary by SKU ID
                sku_id, field = match.groups()

                if field == "product_id":
                    clean_value = int(value)
                elif field == "barcode":
                    clean_value = value
                elif field == "color_id":
                    clean_value = None if value == "" else int(value)
                elif field == "size_id":
                    clean_value = None if value == "" else int(value)
                elif field == "stock_quantity":
                    clean_value = int(value)
                elif field == "special_price":
                    clean_value = None if value == "" else Decimal(value)
                elif field == "status":
                    try:
                        clean_value = SkuStatusEnum(value)
                    except Exception:
                        clean_value = SkuStatusEnum.inactive
                else:
                    skus[sku_id][field] = value

                skus.setdefault(int(sku_id), {})[field] = clean_value

    return skus


def clean_phone_number(phone_number: str) -> str:
    """
    Removes all non-numeric characters from a phone number.

    Parameters:
        phone_number (str): The input phone number string.

    Returns:
        str: A cleaned phone number containing only digits.
    """
    # Regular expression to remove non-numeric characters
    return re.sub(r"\D", "", phone_number)


def get_us_states() -> dict[str, str]:
    """
    Return a dictionary of U.S. mainland states (excluding Alaska, Hawaii, and territories).

    This list can be used to populate select boxes or validate user input
    for addresses and shipping forms.

    Returns:
        dict[str, str]: A dictionary mapping lowercase state keys to their proper names.
    """
    return {
        "alabama": "Alabama",
        "arizona": "Arizona",
        "arkansas": "Arkansas",
        "california": "California",
        "colorado": "Colorado",
        "connecticut": "Connecticut",
        "delaware": "Delaware",
        "florida": "Florida",
        "georgia": "Georgia",
        "idaho": "Idaho",
        "illinois": "Illinois",
        "indiana": "Indiana",
        "iowa": "Iowa",
        "kansas": "Kansas",
        "kentucky": "Kentucky",
        "louisiana": "Louisiana",
        "maine": "Maine",
        "maryland": "Maryland",
        "massachusetts": "Massachusetts",
        "michigan": "Michigan",
        "minnesota": "Minnesota",
        "mississippi": "Mississippi",
        "missouri": "Missouri",
        "montana": "Montana",
        "nebraska": "Nebraska",
        "nevada": "Nevada",
        "new_hampshire": "New Hampshire",
        "new_jersey": "New Jersey",
        "new_mexico": "New Mexico",
        "new_york": "New York",
        "north_carolina": "North Carolina",
        "north_dakota": "North Dakota",
        "ohio": "Ohio",
        "oklahoma": "Oklahoma",
        "oregon": "Oregon",
        "pennsylvania": "Pennsylvania",
        "rhode_island": "Rhode Island",
        "south_carolina": "South Carolina",
        "south_dakota": "South Dakota",
        "tennessee": "Tennessee",
        "texas": "Texas",
        "utah": "Utah",
        "vermont": "Vermont",
        "virginia": "Virginia",
        "washington": "Washington",
        "west_virginia": "West Virginia",
        "wisconsin": "Wisconsin",
        "wyoming": "Wyoming",
    }


def cast_dict_fields_to_int(form_dict: dict, int_fields: list) -> dict:
    for field in int_fields:
        if field in form_dict and form_dict[field].isdigit():
            form_dict[field] = int(form_dict[field])
    return form_dict


def is_dict_empty(data: dict, empty_samples=(None, "", [])) -> bool:
    """
    Check if a dict is empty or all values are in empty_values.
    """
    if not data:
        return True

    for value in data.values():
        if value not in empty_samples:
            return False

    return True
