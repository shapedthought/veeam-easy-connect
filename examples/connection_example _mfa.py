import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
OAuth Authorization with MFA Example - AWS & Azure
This script shows how you can use Veeam Easy Connect to get the MFA token, which you can then
get the code for. Then you can use the code to get the access token.
"""

def main():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    address = input("Enter address: ")

    vec = VeeamEasyConnect(username, password, False) # insecure

    vec.aws().login(address) # or Azure

    your_code = input("Enter your code: ")

    vec.mfa_token_login(your_code) # Will print OK if successful

    token_data = vec.get_access_token()

    print(token_data)

    vec.save_token("token_data")

    vec.save_request_header("request_header")

if __name__ == "__main__":
    main()