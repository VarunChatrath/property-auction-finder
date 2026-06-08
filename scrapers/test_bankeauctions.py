import requests

html = requests.get(
    "https://www.bankeauctions.com/"
).text

print(
    html.count("/immovable-")
)

print(
    html.count("/movable-")
)