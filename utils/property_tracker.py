import pandas as pd
from datetime import datetime
from pathlib import Path

from pathlib import Path

Path("data").mkdir(
    exist_ok=True
)

MASTER_FILE = "data/master_properties.csv"


def get_new_properties(properties):

    master_path = Path(MASTER_FILE)

    try:

        master_df = pd.read_csv(
            MASTER_FILE
        )

    except:

        master_df = pd.DataFrame(
            columns=[
                "property_id",
                "first_seen"
            ]
        )

    existing_ids = set(
        master_df["property_id"].astype(str)
    )

    new_properties = []

    for property_item in properties:

        property_id = str(
            property_item["property_id"]
        )

        if property_id not in existing_ids:

            property_item["first_seen"] = datetime.now()

            new_properties.append(
                property_item
            )

    return new_properties


def update_master_file(new_properties):

    if not new_properties:
        return

    try:

        master_df = pd.read_csv(
            MASTER_FILE
        )

    except:

        master_df = pd.DataFrame(
            columns=["property_id", "first_seen"]
        )

    rows = []

    for property_item in new_properties:

        rows.append({
            "property_id": property_item["property_id"],
            "first_seen": property_item["first_seen"]
        })

    new_df = pd.DataFrame(rows)

    master_df = pd.concat(
        [master_df, new_df],
        ignore_index=True
    )

    master_df.to_csv(
        MASTER_FILE,
        index=False
    )