import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime


BASE_URL = "https://www.eauctionsindia.com"


def search_eauctionsindia_goa():

    auctions = []

    page = 1

    previous_page_ids = set()

    while True:

        if page == 1:
            url = (
                f"{BASE_URL}/properties-in-goa"
            )
        else:
            url = (
                f"{BASE_URL}/properties-in-goa/{page}"
            )

        print(f"\nPage {page}")

        response = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            },
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        cards = soup.find_all(
            "div",
            class_="row mb-3"
        )

        current_page_ids = set()

        page_auctions = []

        found = 0

        for card in cards:

            try:

                text = card.get_text(
                    " ",
                    strip=True
                )

                auction_match = re.search(
                    r"Auction ID\s*:\#\s*(\d+)",
                    text
                )

                if not auction_match:
                    continue

                auction_id = (
                    auction_match.group(1)
                )

                current_page_ids.add(
                    auction_id
                )

                found += 1

                title = ""

                title_tag = card.find("h5")

                if title_tag:

                    title = title_tag.get_text(
                        strip=True
                    )

                reserve_price = ""

                reserve_match = re.search(
                    r"Reserve Price\s*:\s*(₹[\d,\.]+)",
                    text
                )

                if reserve_match:

                    reserve_price = (
                        reserve_match.group(1)
                    )

                detail_url = (
                    f"{BASE_URL}/properties/{auction_id}"
                )

                page_auctions.append({

                    "source":
                    "EAUCTIONSINDIA",

                    "unique_id":
                    f"EI_{auction_id}",

                    "property_id":
                    auction_id,

                    "bank_name":
                    "",

                    "property_title":
                    title,

                    "city":
                    "Goa",

                    "reserve_price":
                    reserve_price,

                    "auction_date":
                    "",

                    "details_url":
                    detail_url,

                    "date_found":
                    datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                })

            except Exception as e:

                print(
                    "Card Error:",
                    e
                )

        print(
            f"Found {found} listings"
        )

        if found == 0:

            print(
                "No listings found."
            )

            break

        if (
            current_page_ids
            ==
            previous_page_ids
        ):

            print(
                "Duplicate page detected."
            )

            print(
                "Last page reached."
            )

            break

        auctions.extend(
            page_auctions
        )

        previous_page_ids = (
            current_page_ids
        )

        page += 1

    # Final safety dedupe

    unique_rows = {}

    for row in auctions:

        unique_rows[
            row["unique_id"]
        ] = row

    auctions = list(
        unique_rows.values()
    )

    print(
        f"\nTotal Auctions: {len(auctions)}"
    )

    return auctions


if __name__ == "__main__":

    data = (
        search_eauctionsindia_goa()
    )

    print()

    print(
        f"Total Records: {len(data)}"
    )

    if data:

        print(
            "\nSample Record:"
        )

        print(data[0])