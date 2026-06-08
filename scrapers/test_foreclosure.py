import requests
from bs4 import BeautifulSoup

url = "https://foreclosureindia.com/bank-auctions/goa/2"

html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

rows = soup.find_all("tr")

print("Rows:", len(rows))

for row in rows[:3]:
    print("-" * 50)
    print(row.get_text(" ", strip=True))