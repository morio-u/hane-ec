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
