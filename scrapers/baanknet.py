import requests
from datetime import datetime
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

URL = (
    "https://baanknet.com/eauction-psb/api/"
    "property-listing-data/1?page=0&size=100"
)


def search_baanknet_goa():

    payload = {
        "state": "Goa",
        "stateId": 10,
        "cityId": None,
        "city": "",
        "searchType": "",
        "priceFrom": "10000000",
        "priceTo": "50000000000",
        "sortBy": "3"
    }

    response = requests.post(
        URL,
        json=payload,
        timeout=30,
        verify=False
    )

    response.raise_for_status()

    data = response.json()

    properties = []

    for row in data["data"]:

        properties.append({

            "source":
                "BAANKNET",

            "unique_id":
                f"BN_{row['propertyId']}",

            "property_id":
                row.get("propertyId"),

            "bank_name":
                row.get("bankName"),

            "property_title":
                row.get("propertySubType"),

            "city":
                row.get("city"),

            "district":
                row.get("districtname"),

            "reserve_price":
                row.get("price"),

            "auction_date":
                row.get("auctionEndDateTime"),

            "property_type":
                row.get("typeOfAsset"),

            "possession_type":
                row.get("possessionType"),

            "address":
                row.get("address"),

            "posted_on":
                row.get("postedOn"),

            "website":
                "https://baanknet.com/property-listing",

            "date_found":
                datetime.now().strftime("%Y-%m-%d")
        })

    return properties


if __name__ == "__main__":

    properties = search_baanknet_goa()

    print()
    print(
        f"Total Properties: {len(properties)}"
    )

    if properties:

        print()
        print("Sample Record:")
        print(properties[0])

    import pandas as pd

    df = pd.DataFrame(
        properties
    )

    df.to_csv(
        "output/baanknet_goa.csv",
        index=False
    )

    print()
    print(
        "Saved: output/baanknet_goa.csv"
    )