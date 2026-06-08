import requests
import pandas as pd
from datetime import datetime

URL = (
    "https://www.bankeauctions.com/home/liveAuctionDatatable/"
    "?reservePriceMaxRange="
    "&reservePriceMinRange=0"
    "&state=6"
    "&propertytype=null"
    "&tmpAct=0"
    "&search_input="
    "&city_name=goa"
    "&bank_id=Organisation/Bank%20Name"
    "&property_sub_type=null"
    "&budget_search=Budget"
)

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def search_bankeauctions_goa():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    auctions = []

    for row in data["aaData"]:

        category = str(
            row[12]
        ).lower()

        subcategory = str(
            row[13]
        ).lower()

        city_slug = (
            str(row[4])
            .lower()
            .replace(" ", "-")
        )

        product_id = row[10]

        property_description = (
            str(row[3])
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
        )

        details_url = (
            f"https://www.bankeauctions.com/"
            f"{category}-"
            f"{subcategory}-"
            f"{city_slug}-"
            f"{product_id}"
        )

        auctions.append({

    "unique_id":
    f"BA_{row[1]}",

    "source":
    "BankeAuctions",

    "auction_id":
    row[1],

    "product_id":
    product_id,

    "bank_name":
    row[2],

    "property_description":
    property_description,

    "city":
    row[4],

    "bid_last_date":
    row[5],

    "reserve_price":
    str(row[6]),

    "emd":
    str(row[7]),

    "event_type":
    row[8],

    "property_category":
    row[12],

    "property_sub_category":
    row[13],

    "details_url":
    details_url,

    "date_found":
    datetime.now().strftime("%Y-%m-%d")
})

    return auctions


if __name__ == "__main__":

    try:

        auctions = (
            search_bankeauctions_goa()
        )

        print()
        print(
            f"Total Auctions: {len(auctions)}"
        )

        df = pd.DataFrame(
            auctions
        )

        df.to_csv(
            "output/bankeauctions_goa.csv",
            index=False
        )

        print()
        print(
            "Saved: output/bankeauctions_goa.csv"
        )

        print()

        if len(auctions) > 0:

            print(
                "Sample Record:"
            )

            print(
                auctions[0]
            )

    except Exception as e:

        print(
            "Error:"
        )

        print(e)