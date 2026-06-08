import requests
import json
import pandas as pd

url = "https://ibapi.in/Sale_Info_Home.aspx/Button_search_Click"

payload = {
    "key_val": [
        ["State", "'GA'"]
    ]
}

headers = {
    "Content-Type": "application/json; charset=utf-8"
}

response = requests.post(
    url,
    json=payload,
    headers=headers
)

data = response.json()

records = json.loads(data["d"])

df = pd.DataFrame(records)

print(df.head())

df.to_csv(
    "output/goa_raw.csv",
    index=False
)

print(f"Total Properties: {len(df)}")