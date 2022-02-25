import json
import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
Getting Repository Information from the Veeam API (OAuth) with inline authentication
This script shows how authenticate with the API, then send a request to get and save the repositories 
from VBR in one script.

Uses the short request URL version
"""

def main():
    address = input("Enter address: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")

    vec = VeeamEasyConnect(username, password, False) # insecure

    vec.vbr().login(address)

    # short URL version
    url = "backupInfrastructure/repositories"

    # requires the "False" parameter passed
    res_data = vec.get(url, full=False)

    with open("repos.json", "w") as repos_json:
        json.dump(res_data, repos_json)


if __name__ == "__main__":
    main()