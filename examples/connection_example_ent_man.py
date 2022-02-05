import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
Basic Authorization with Enterprise Manager
This script shows how you can use Veeam Easy Connect to get the Token from the API 
and then save it to a json file for future use.
"""

def main():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter password: ")
    address = input("Enter address: ")

    vec = VeeamEasyConnect(username, password, False) # insecure

    vec.ent_man().login(address)

    token_data = vec.get_access_token()

    print(token_data)

    vec.save_token("token_data")

    vec.save_request_header("request_header")

if __name__ == "__main__":
    main()