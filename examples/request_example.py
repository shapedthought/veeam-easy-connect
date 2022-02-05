import json
import requests
import urllib3
urllib3.disable_warnings()
import pprint

"""
Getting Repository Information from the Veeam API (OAuth)
This script shows how to open and grab the data from the header file and add it directly to the request.
It then shows how to send the data to the API and how to handle the response, saving it to another JSON file.
"""

def main():
    address = input("Enter address: ")

    with open("request_header.json", "r") as token_data:
        header = json.load(token_data)

    url = f"https://{address}:9419/api/v1/backupInfrastructure/repositories"

    res = requests.get(url, headers=header, verify=False)

    res.raise_for_status()

    data = res.json()

    pprint.pprint(data)

    with open("repos.json", "w") as repos_json:
        json.dump(data, repos_json)

if __name__ == "__main__":
    main()