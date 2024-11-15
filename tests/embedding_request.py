from pprint import pprint
import requests

API_URL = "https://api-inference.huggingface.co/models/intfloat/multilingual-e5-large-instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Today is a sunny day and I will get some ice cream."
})

pprint(output[0])


# [-0.003874944057315588,
#  0.032939717173576355,
#  -0.015217156149446964,