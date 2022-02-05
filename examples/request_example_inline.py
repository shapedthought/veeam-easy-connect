import json
import requests
import urllib3
urllib3.disable_warnings()
import pprint
import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
Getting Repository Information from the Veeam API (OAuth) with inline authentication
This script shows how authenticate with the API, then send a request to get and save the repositories 
from VBR in one script.
"""

def main():
    address = input("Enter address: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")

    vec = VeeamEasyConnect(username, password, False) # insecure

    vec.vbr().login(address)

    url = f"https://{address}:9419/api/v1/backupInfrastructure/repositories"

    res_data = vec.get(url)

    with open("repos.json", "w") as repos_json:
        json.dump(res_data, repos_json)


if __name__ == "__main__":
    main()