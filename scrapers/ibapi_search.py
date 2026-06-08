import requests
import json
import pandas as pd
import re
from datetime import datetime

SEARCH_URL = "https://ibapi.in/Sale_Info_Home.aspx/Button_search_Click"


def search_properties(filters):

    payload = {
        "key_val": filters
    }

    response = requests.post(
        SEARCH_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    records = json.loads(
        data["d"]
    )

    cleaned_records = []

    for record in records:

        property_html = record.get(
            "Property ID",
            ""
        )

        match = re.search(
            r'>(.*?)<',
            property_html
        )

        property_id = (
            match.group(1)
            if match
            else ""
        )

        details_url = (
            "https://www.mstcecommerce.com/"
            f"auctionhome/ibapi/index.jsp?property_id={property_id}"
        )

        cleaned_records.append({
             "unique_id":
    f"IBAPI_{property_id}",
            "property_id": property_id,
            "bank_name": record.get("Bank Name"),
            "property_type": record.get("Property"),
            "reserve_price": record.get("Reserve Price (Rs)"),
            "state": record.get("State"),
            "district": record.get("District"),
            "city": record.get("City"),
            "rowid": record.get("ROWID"),
            "details_url": details_url,
            "date_found":datetime.now().strftime("%Y-%m-%d")
        })

    return cleaned_records


def search_goa():

    filters = [
        ["State", "'GA'"]
    ]

    return search_properties(
        filters
    )


def search_alibaug():

    filters = [
        ["State", "'MH'"],
        ["District", "'520'"],
        ["City", "'ALIBAUG'"]
    ]

    return search_properties(
        filters
    )


if __name__ == "__main__":

    goa = search_goa()

    print(
        f"Goa Properties: {len(goa)}"
    )

    alibaug = search_alibaug()

    print(
        f"Alibaug Properties: {len(alibaug)}"
    )

    all_properties = (
        goa + alibaug
    )

    df = pd.DataFrame(
        all_properties
    )

    print(df.head())