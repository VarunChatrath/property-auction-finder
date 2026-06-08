import pandas as pd
import os

MASTER_FILE = "data/master_auctions.csv"


def get_new_auctions(all_auctions):

    if not os.path.exists(MASTER_FILE):

        return all_auctions

    try:

        master_df = pd.read_csv(
            MASTER_FILE
        )

        existing_ids = set(
            master_df["unique_id"]
        )

    except:

        return all_auctions

    new_auctions = []

    for auction in all_auctions:

        if (
            auction["unique_id"]
            not in existing_ids
        ):

            new_auctions.append(
                auction
            )

    return new_auctions


def update_master_file(
    all_auctions
):

    rows = []

    for auction in all_auctions:

        rows.append({
            "unique_id":
            auction["unique_id"]
        })

    df = pd.DataFrame(
        rows
    )

    os.makedirs(
        "data",
        exist_ok=True
    )

    df.to_csv(
        MASTER_FILE,
        index=False
    )