import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
import json

class VeeamEasyConnect:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
    
    def basic_auth(self, address: str) -> dict:
        self.basic_headers = {
             "accept": "application/json",
        }

        self.basic_url = f"https://{address}:9398/api/sessionMngr/?v=latest"
        self.b_auth = HTTPBasicAuth(self.username, self.password)
        self.response = requests.post(self.basic_url, headers=self.basic_headers, auth=self.b_auth, verify=False)
        self.response.raise_for_status()
        self.res_json_basic = self.response.json()


    def oauth_login(self, address: str) -> dict:
        self.oauth_headers = {
            "accept": "application/json",
            "x-api-version": "1.0-rev1", 
            "Content-Type": "application/x-www-form-urlencoded"}

        self.oauth_url = f"https://{address}:9419/api/oauth2/token"

        self.oauth_data = {
            "grant_type" : "password", 
            "username" : self.username,
            "password": self.password
            }
        self.response = requests.post(self.oauth_url, data=self.oauth_data, headers=self.oauth_headers, verify=False)
        self.response.raise_for_status()
        self.res_json_oauth = self.response.json()


    def save_data(self, auth_type: str, file_name: str) -> None:
        if auth_type == "basic":
            data = self.res_json_basic
        elif auth_type == "oauth":
            data = self.res_json_oauth
        
        with open(f"{file_name}.json", "w") as token_file:
            json.dump(data, token_file)

    def get_json_data(self, json_type: str) -> dict:
        if json_type == "basic":
            return self.res_json_basic
        elif json_type == "oauth":
            return self.res_json_oauth
        else:
            print("Type not recognized; please use either basic or oauth")
            return
