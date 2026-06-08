import re

def extract_area_acres(text):

    if not text:
        return None

    pattern = r'(\d+(?:\.\d+)?)\s*(?:sq\.?\s*mtr|sq\.?\s*mtrs|sq\.?\s*mts|sq\s*m|sqm)'

    match = re.search(
        pattern,
        text.lower()
    )

    if not match:
        return None

    sqm = float(match.group(1))

    acres = sqm / 4046.86

    return round(acres, 2)