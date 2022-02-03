import json
import requests
import urllib3
urllib3.disable_warnings()
import pprint

"""
Getting Repository Information from the Veeam API (OAuth)
This script shows how to open and grab the data from the token file, then add it to the request header.
It then shows how to send the data to the API and how to handle the response, saving it to another JSON file.
"""

address = "YOUR_ADDRESS"

with open("tokendata.json", "r") as token_data:
    token_dict = json.load(token_data)

token = token_dict.get("access_token")

headers = {
    	"accept": "application/json",
        "x-api-version": "1.0-rev1",
	    "Authorization": "Bearer " + token
}

url = f"https://{address}:9419/api/v1/backupInfrastructure/repositories"

res = requests.get(url, headers=headers, verify=False)

res.raise_for_status()

data = res.json()

pprint.pprint(data)

with open("repos.json", "w") as repos_json:
    json.dump(data, repos_json)