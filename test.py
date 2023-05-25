import requests
import json

url = "https://sandbox-merchant.revolut.com/api/1.0/orders"

payload = json.dumps({
  "amount": 777,
  "currency": "USD",
  "email": "johndddddddoe001@gmail.com"
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'sk_zWT17VD9v8ukRyhAgTA4HSmqPuq8TQjk_97xukS740i4F7cA2GPiwDOZOWpOLzyu'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)