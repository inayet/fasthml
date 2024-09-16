import requests, json

vin1 = "1HGCR2F82EA086751"
vin2 = "2T1BURHE0KC218711"
url = (
    f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/{vin2}?format=json"
)
r = requests.get(url)
# print(r.text.replace("'", '"'));
print(json.dumps(r.json(), indent=4))
