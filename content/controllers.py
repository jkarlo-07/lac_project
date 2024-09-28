import requests
from .config import PAYMONGO_API_KEY, PAYMONGO_API_URL
import base64

def encode_api_key(api_key):
    return base64.b64encode(api_key.encode()).decode()

encoded_key = encode_api_key(PAYMONGO_API_KEY)

def create_payment_link(amount, description ,remarks):
    payload = { "data": { "attributes": {
            "amount": amount,
            "description": description,
            "remarks": remarks
        } } }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {encoded_key}"
    }

    response = requests.post(PAYMONGO_API_URL, json=payload, headers=headers)
    return response.json()