import requests, json

vin = "1HGCR2F82EA086751"
url = (
    f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/{vin}?format=json"
)
r = requests.get(url)
# print(r.text.replace("'", '"'));
print(json.dumps(r.json(), indent=4))
