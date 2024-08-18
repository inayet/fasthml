import requests

url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"
post_fields = {"format": "json", "data": "5NTJCDAE7PH052205"}
r = requests.post(url, data=post_fields)
print(r.text)
