import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
OAuth Authorization with MFA Example - AWS & Azure
This script shows how you can use Veeam Easy Connect to get the MFA token, which you can then
get the code for. Then you can use the code to get the access token.
"""

def main():
    username = "YOUR_USERNAME"
    password = getpass.getpass("Enter password: ")
    address = "YOUR_ADDRESS"

    vec = VeeamEasyConnect(username, password)

    vec.oauth_login(address, "aws") # 

    vec.get_mfa_token() # This will print the mfa token

    your_code = input("Enter your code: ")

    vec.mfa_token_login(your_code) # Will print OK if successful

    token_data = vec.get_json_data("oauth")

    print(token_data)

    vec.save_data("oauth", "tokendata")

if __name__ == "__main__":
    main()