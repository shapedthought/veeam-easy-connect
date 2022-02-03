import getpass
from veeam_easy_connect import VeeamEasyConnect

"""
OAuth Authorization Example
This script shows how you can use Veeam Easy Connect to get the Token from the API 
and then save it to a json file for future use.
"""

username = "USERNAME"
password = getpass.getpass("Enter password: ")
url = "YOUR_ADDRESS"

vec = VeeamEasyConnect(username, password)

vec.oauth_login(url)

print(vec.res_json_oauth)

vec.save_data("oauth", "tokendata")