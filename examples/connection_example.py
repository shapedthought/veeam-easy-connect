import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
OAuth Authorization Example
This script shows how you can use Veeam Easy Connect to get the Token from the API 
and then save it to a json file for future use.
"""

username = "YOUR_USERNAME"
password = getpass.getpass("Enter password: ")
address = "YOUR_ADDRESS"

vec = VeeamEasyConnect(username, password)

vec.oauth_login(address)

token_data = vec.get_json_data("oauth")

print(token_data)

vec.save_data("oauth", "tokendata")