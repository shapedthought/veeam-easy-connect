import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
Basic Authorization Example (Enterprise Manager)
This script shows how you can use Veeam Easy Connect to get the Token from the API 
and then save it to a json file for future use.
"""

def main():
    username = "YOUR_USERNAME"
    password = getpass.getpass("Enter password: ")
    address = "YOUR_ADDRESS"

    vec = VeeamEasyConnect(username, password)

    vec.basic_auth(address)

    token_data = vec.get_access_token("basic")

    print(token_data)

    vec.save_data("basic", "tokendata")

if __name__ == "__main__":
    main()