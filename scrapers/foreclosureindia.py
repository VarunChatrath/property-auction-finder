import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


BASE_URL = "https://foreclosureindia.com/bank-auctions/goa"


def search_foreclosure_goa():

    all_properties = []

    page = 1

    while True:

        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}/{page}"

        print(f"Scraping Page {page}")

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        rows = soup.find_all("tr")

        if len(rows) <= 1:
            break

        page_records = 0

        for row in rows[1:]:

            cols = row.find_all("td")

            if len(cols) < 7:
                continue

            listing_id = cols[0].get_text(
                strip=True
            )

            bank_name = cols[1].get_text(
                strip=True
            )

            property_name = cols[2].get_text(
                strip=True
            )

            application_deadline = cols[3].get_text(
                strip=True
            )

            auction_date = cols[4].get_text(
                strip=True
            )

            reserve_price = cols[5].get_text(
                strip=True
            )

            link_tag = cols[6].find("a")

            details_url = None

            if link_tag:
                details_url = link_tag.get(
                    "href"
                )

            location = ""

            if " in " in property_name:
                location = property_name.split(" in ")[-1].strip()    

            all_properties.append({
                "unique_id":
    f"FCI_{listing_id}",
    "source": "ForeclosureIndia",
    "listing_id": listing_id,
    "bank_name": bank_name,
    "property_name": property_name,
    "location": location,
    "application_deadline": application_deadline,
    "auction_date": auction_date,
    "reserve_price": reserve_price,
    "details_url": details_url,
    "date_found": datetime.now().strftime("%Y-%m-%d")
})

            page_records += 1

        print(
            f"Found {page_records} auctions"
        )

        page += 1

    return all_properties


if __name__ == "__main__":

    properties = search_foreclosure_goa()

    print()
    print(
        f"Total Auctions: {len(properties)}"
    )

    print()

    if properties:
        print(properties[0])

    df = pd.DataFrame(
        properties
    )

    df.to_csv(
        "output/foreclosure_goa.csv",
        index=False
    )

    df.to_excel(
        "output/foreclosure_goa.xlsx",
        index=False
    )

    print()
    print(
        "Saved: output/foreclosure_goa.csv"
    )

    print(
        "Saved: output/foreclosure_goa.xlsx"
    )