import pandas as pd
import os

from scrapers.ibapi_search import (
    search_goa,
    search_alibaug
)

from scrapers.eauctionsindia import (
    search_eauctionsindia_goa
)

from scrapers.foreclosureindia import (
    search_foreclosure_goa
)

from scrapers.bankeauctions import (
    search_bankeauctions_goa
)

from scrapers.ibapi_documents import (
    get_property_documents
)

from utils.master_tracker import (
    get_new_auctions,
    update_master_file
)

from scrapers.baanknet import (
    search_baanknet_goa
)

# ------------------------------------
# IBAPI
# ------------------------------------

print("Getting IBAPI auctions...")

goa = search_goa()
alibaug = search_alibaug()

ibapi_all = goa + alibaug

for i, record in enumerate(ibapi_all):

    property_id = record["property_id"]

    print(
        f"{i+1}/{len(ibapi_all)} : {property_id}"
    )

    docs = get_property_documents(
        property_id
    )

    record.update(docs)

# ------------------------------------
# CLEAN IBAPI
# ------------------------------------

ibapi_clean = []

for row in ibapi_all:

    ibapi_clean.append({

        "source":
        "IBAPI",

        "unique_id":
        row["unique_id"],

        "bank_name":
        row["bank_name"],

        "property_title":
        row["property_type"],

        "city":
        row["city"],

        "reserve_price":
        row["reserve_price"],

        "auction_date":
        "",

        "details_url":
        row["details_url"],

        "pdf_url":
        row.get("pdf_url", ""),

       

        "date_found":
        row["date_found"]
    })

print()
print("Getting BAANKNET auctions...")

baanknet = search_baanknet_goa()

# ------------------------------------
# EAUCTIONSINDIA
# ------------------------------------

print()
print("Getting EAuctionsIndia auctions...")

eauctions = search_eauctionsindia_goa()


# ------------------------------------
# FORECLOSURE INDIA
# ------------------------------------

print()
print("Getting ForeclosureIndia auctions...")

foreclosure = search_foreclosure_goa()

# ------------------------------------
# CLEAN FORECLOSURE INDIA
# ------------------------------------

foreclosure_clean = []

for row in foreclosure:

    foreclosure_clean.append({

        "source":
        "ForeclosureIndia",

        "unique_id":
        row["unique_id"],

        "bank_name":
        row["bank_name"],

        "property_title":
        row["property_name"],

        "city":
        "",

        "reserve_price":
        row["reserve_price"],

        "auction_date":
        row["auction_date"],

        "details_url":
        row["details_url"],

        "pdf_url":
        "",

        

        "date_found":
        row["date_found"]
    })

# ------------------------------------
# BANKEAUCTIONS
# ------------------------------------

print()
print("Getting BankeAuctions auctions...")

banke = search_bankeauctions_goa()

# ------------------------------------
# CLEAN BANKEAUCTIONS
# ------------------------------------

banke_clean = []

for row in banke:

    banke_clean.append({

        "source":
        "BankeAuctions",

        "unique_id":
        row["unique_id"],

        "bank_name":
        row["bank_name"],

        "property_title":
        row["property_description"][:100],

        "city":
        row["city"],

        "reserve_price":
        row["reserve_price"],

        "auction_date":
        row["bid_last_date"],

        "details_url":
        row["details_url"],

        "pdf_url":
        "",

        

        "date_found":
        row["date_found"]
    })

# ------------------------------------
# MERGE ALL
# ------------------------------------

all_auctions = (
    ibapi_clean
    + foreclosure_clean
    + banke_clean
     + baanknet
     + eauctions
)

print()
print("=" * 50)
print("SUMMARY")
print("=" * 50)

print(f"IBAPI: {len(ibapi_clean)}")
print(f"ForeclosureIndia: {len(foreclosure_clean)}")
print(f"BankeAuctions: {len(banke_clean)}")
print(f"BAANKNET: {len(baanknet)}")
print(f"EAUCTIONSINDIA: {len(eauctions)}")
print(f"Total Auctions: {len(all_auctions)}")

# ------------------------------------
# FIND NEW AUCTIONS
# ------------------------------------

new_auctions = get_new_auctions(
    all_auctions
)

print(
    f"New Auctions: {len(new_auctions)}"
)

# ------------------------------------
# SAVE FILES
# ------------------------------------

os.makedirs(
    "output",
    exist_ok=True
)

# ------------------------------------
# CLEAN ALL AUCTIONS DATAFRAME
# ------------------------------------

all_df = pd.DataFrame(
    all_auctions
)

required_columns = [

    "source",
    "unique_id",
    "bank_name",
    "property_title",
    "city",
    "reserve_price",
    "auction_date",
    "details_url",
    "date_found"
]

for col in required_columns:

    if col not in all_df.columns:

        all_df[col] = ""

all_df = all_df[
    required_columns
]

all_df["bank_name"] = (
    all_df["bank_name"]
    .fillna("")
)

all_df["city"] = (
    all_df["city"]
    .fillna("")
)

all_df["auction_date"] = (
    all_df["auction_date"]
    .fillna("")
)

all_df["property_title"] = (
    all_df["property_title"]
    .fillna("")
)

all_df["reserve_price"] = (
    all_df["reserve_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

all_df["reserve_price"] = pd.to_numeric(
    all_df["reserve_price"],
    errors="coerce"
)

all_df = all_df.drop_duplicates(
    subset=["unique_id"]
)

all_df = all_df.sort_values(
    by="reserve_price",
    ascending=False
)

print(
    f"Final Clean Records: {len(all_df)}"
)

# ------------------------------------
# CLEAN NEW AUCTIONS DATAFRAME
# ------------------------------------

new_df = pd.DataFrame(
    new_auctions
)

for col in required_columns:

    if col not in new_df.columns:

        new_df[col] = ""

new_df = new_df[
    required_columns
]

new_df["reserve_price"] = (
    new_df["reserve_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

new_df["reserve_price"] = pd.to_numeric(
    new_df["reserve_price"],
    errors="coerce"
)

new_df = new_df.sort_values(
    by="reserve_price",
    ascending=False
)
all_df.to_excel(
    "output/all_auctions.xlsx",
    index=False
)

new_df.to_excel(
    "output/new_auctions.xlsx",
    index=False
)

# ------------------------------------
# UPDATE MASTER
# ------------------------------------

update_master_file(
    all_auctions
)

print()
print(
    "Saved: output/all_auctions.xlsx"
)

print(
    "Saved: output/new_auctions.xlsx"
)