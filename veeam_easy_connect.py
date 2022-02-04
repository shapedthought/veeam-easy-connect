from sys import api_version
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
import json

"""
Veeam Easy Connect
This module does all the set up to allow you to connect to Veeam APIs
"""
class VeeamEasyConnect:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.oauth_headers = {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
            }
        self.get_settings()
    
    def basic_auth(self, address: str) -> None:
        self.basic_headers = {
             "accept": "application/json",
        }

        self.basic_url = f"https://{address}:9398/api/sessionMngr/?v=latest"
        self.b_auth = HTTPBasicAuth(self.username, self.password)
        self.response = requests.post(self.basic_url, headers=self.basic_headers, auth=self.b_auth, verify=False)
        self.response.raise_for_status()
        if self.response.status_code == 200:
            print("OK")
        self.basic_id = self.response.headers["X-RestSvcSessionId"]
        self.res_json_basic = self.response.json()

    def oauth_login(self, address: str, api_type: str) -> None:
        # set up each login url endpoint and api version
        self.update_settings(api_type)
        self.address = address
        self.oauth_url = f"https://{self.address}{self.url_end}"
        self.oauth_data = {
            "grant_type" : "password", 
            "username" : self.username,
            "password": self.password
            }
        self.response = requests.post(self.oauth_url, data=self.oauth_data, headers=self.oauth_headers, verify=False)
        self.response.raise_for_status()
        if self.response.status_code == 200:
            print("OK")
        self.res_json_oauth = self.response.json()

    def mfa_token_login(self, code: str) -> None:
        self.token = self.res_json_mfa_oauth['mfa_token']
        self.mfa_url = f"https://{self.address}{self.url_end}"
        self.mfa_data = {
            "grant_type": "mfa",
            "mfa_token":  self.token,
            "mfa_code": code
        }
        # I don't think I need to change the Content-Type on this request- not clear
        self.mfa_response = requests.post(self.mfa_url, data=self.oauth_data, headers=self.oauth_headers, verify=False)
        self.response.raise_for_status()
        if self.response.status_code == 200:
            print("OK")
        self.res_json_oauth = self.response.json()


    def save_data(self, auth_type: str, file_name: str) -> None:
        # Added a check in case extension was included
        file_name = file_name.split(".")[0] if "." in file_name else file_name

        if auth_type == "basic":
            data = self.response.headers
        elif auth_type == "oauth":
            data = self.res_json_oauth
        else:
            print("Type not recognized; please use basic, or oauth")
            return
        with open(f"{file_name}.json", "w") as token_file:
            json.dump(data, token_file)

    def get_body_data(self, json_type: str) -> dict:
        if json_type == "basic":
            return self.res_json_basic
        elif json_type == "oauth":
            return self.res_json_oauth
        else:
            print("Type not recognized; please use either basic or oauth")
            return

    def get_header_data(self) -> dict:
        return self.response.headers

    def get_access_token(self, token_type="oauth") -> str:
        if token_type == "basic":
            return self.basic_id
        else: 
            return self.res_json_oauth['access_token']

    def get_access_token_with_bearer(self) -> str:
        token = self.res_json_oauth['access_token']
        return f"Bearer " + token

    def get_mfa_token(self) -> None:
        print(self.res_json_oauth['mfa_token'])

    # load in data from the settings file - makes this easier to update
    def get_settings(self) -> None:
        with open("api_settings.json", "r") as settings_file:
            self.api_settings = json.load(settings_file)

    # Update the URL and headers as needed
    def update_settings(self, api_type: str) -> None:
        if api_type == "o365":
            self.url_end = self.api_settings['o365']['url']
            # No API version specified in the documentation
        elif api_type == "aws":
            self.url_end = self.api_settings['aws']['url']
            self.oauth_headers = self.api_settings['aws']['headers']
        elif api_type == "vbr":
            self.url_end = self.api_settings['vbr']['url']
            self.oauth_headers = self.api_settings['vbr']['headers']
        elif api_type == "azure":
            self.url_end = self.api_settings['azure']['url']
            self.oauth_headers = self.api_settings['azure']['headers']
        elif api_type == "gcp":
            self.url_end = self.api_settings['gcp']['url']
            self.oauth_headers = self.api_settings['gcp']['headers']
        else:
            print("API type not found")
            return

