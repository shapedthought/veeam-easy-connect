import json
import requests
import urllib3
urllib3.disable_warnings()
import pprint
import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
Getting Repository Information from the Veeam API (OAuth) with inline authentication
This script shows how authenticate with the API, then send a request to get and save the repositories from VBR in one script.
"""

def main():
    address = "YOUR_ADDRESS"
    username = "YOUR_USERNAME"
    password = getpass.getpass("Enter Password: ")

    vec = VeeamEasyConnect(username, password, False) # insecure

    vec.vbr().login(address)

    token = vec.get_access_token_with_bearer()

    headers = {
            "accept": "application/json",
            "x-api-version": "1.0-rev1",
            "Authorization": token
    }

    url = f"https://{address}:9419/api/v1/backupInfrastructure/repositories"

    res = requests.get(url, headers=headers, verify=False)

    res.raise_for_status()

    data = res.json()

    pprint.pprint(data)

    with open("repos.json", "w") as repos_json:
        json.dump(data, repos_json)


if __name__ == "__main__":
    main()