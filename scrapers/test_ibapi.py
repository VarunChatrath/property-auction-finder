# scrapers/test_ibapi.py
print("Script Started")
import requests
import json

url = "https://ibapi.in/Sale_Info_Home.aspx/Button_search_Click"

payload = {
    "key_val": [
        ["State", "'GA'"]
    ]
}

response = requests.post(url, json=payload)

data = response.json()

records = json.loads(data["d"])

print(f"Properties Found: {len(records)}")

print(records[0])