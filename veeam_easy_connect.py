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
    def __init__(self, username, password, verify=True) -> None:
        self.username = username
        self.password = password
        self.verify = verify
        self.oauth_headers = {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
            }
        self.__get_settings()
        self.basic = False
        self.api_type = ""
    
    def __em_login(self, address: str) -> None:
        self.basic = True
        self.basic_headers = {
             "accept": "application/json",
        }

        self.basic_url = f"https://{address}:9398/api/sessionMngr/?v=latest"
        self.b_auth = HTTPBasicAuth(self.username, self.password)
        self.response = requests.post(self.basic_url, headers=self.basic_headers, auth=self.b_auth, verify=self.verify)
        self.response.raise_for_status()
        if self.response.status_code == 201:
            print("OK")
        self.basic_id = self.response.headers["X-RestSvcSessionId"]
        self.res_json_basic = self.response.json()
        self.reqest_header = self.get_request_header()

    def login(self, address: str) -> None:
        if self.basic:
            self.__em_login(address)
        else:
        # set up each login url endpoint and api version
            self.address = address
            self.oauth_url = f"https://{self.address}{self.url_end}"
            self.oauth_data = {
                "grant_type" : "password", 
                "username" : self.username,
                "password": self.password
                }
            self.response = requests.post(self.oauth_url, data=self.oauth_data, headers=self.oauth_headers, verify=self.verify)
            self.response.raise_for_status()
            if self.response.status_code == 200:
                print("OK")
            self.res_json_oauth = self.response.json()
            self.reqest_header = self.get_request_header()

    def mfa_token_login(self, code: str) -> None:
        self.token = self.res_json_mfa_oauth['mfa_token']
        self.mfa_url = f"https://{self.address}{self.url_end}"
        self.mfa_data = {
            "grant_type": "mfa",
            "mfa_token":  self.token,
            "mfa_code": code
        }
        # I don't think I need to change the Content-Type on this request- not clear
        self.mfa_response = requests.post(self.mfa_url, data=self.oauth_data, headers=self.oauth_headers, verify=self.verify)
        self.response.raise_for_status()
        if self.response.status_code == 200:
            print("OK")
        self.res_json_oauth = self.response.json()        

    def save_token(self, file_name: str) -> None:
        # Added a check in case extension was included
        file_name = file_name.split(".")[0] if "." in file_name else file_name

        if self.basic:
            data = self.response.headers
        else:
            data = self.res_json_oauth
        with open(f"{file_name}.json", "w") as token_file:
            json.dump(data, token_file)

    def get_body_data(self) -> dict:
        if self.basic:
            return self.res_json_basic
        else:
            return self.res_json_oauth

    def get_header_data(self) -> dict:
        return self.response.headers

    def get_access_token(self) -> str:
        if self.basic:
            return self.basic_id
        else: 
            return self.res_json_oauth['access_token']

    def get_request_header(self) -> dict:
        if self.api_type == "ent_man":
            headers = {
                "accept": "application/json",
                "X-RestSvcSessionId": self.basic_id
            }
        else:
            headers = self.api_settings[self.api_type]['headers']
            if "Content-type" in headers:
                headers.pop('Content-type')
            bearer_string = 'Bearer ' + self.res_json_oauth['access_token']
            headers['Authorization'] = bearer_string
        return headers
    
    def save_request_header(self, file_name: str) -> None:
        file_name = file_name.split(".")[0] + ".json" if "." in file_name else file_name + ".json"
        headers = self.get_request_header()
        with open(file_name, "w") as headers_file:
            json.dump(headers, headers_file)

    def get_access_token_with_bearer(self) -> str:
        if self.basic:
            return self.basic_id
        else:
            token = self.res_json_oauth['access_token']
            return f"Bearer " + token

    def get_mfa_token(self) -> None:
        print(self.res_json_oauth['mfa_token'])

    # load in data from the settings file - makes this easier to update
    def __get_settings(self) -> None:
        with open("api_settings.json", "r") as settings_file:
            self.api_settings = json.load(settings_file)

    def aws(self):
        self.update_settings("aws")
        self.api_type = "aws"
        return self

    def gcp(self):
        self.update_settings("gcp")
        self.api_type = "gcp"
        return self

    def azure(self):
        self.update_settings("azure")
        self.api_type = "azure"
        return self

    def vbr(self):
        self.update_settings("vbr")
        self.api_type = "vbr"
        return self

    def o365(self):
        self.update_settings("o365")
        self.api_type = "o365"
        return self

    def ent_man(self):
        self.basic = True
        self.api_type = "ent_man"
        return self
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

    def get(self, url: str) -> dict:
        resp = requests.get(url, headers=self.reqest_header, verify=self.verify)
        resp.raise_for_status()
        if resp.status_code == 200:
            print("OK")
        return resp.json()

    def post(self, url: str, data: dict) -> dict:
        resp = requests.post(url, headers=self.reqest_header, data=data, verify=self.verify)
        resp.raise_for_status()
        print(resp.status_code)
        return resp.json()

    def put(self, url: str, data: dict) -> dict:
        resp = requests.put(url, headers=self.reqest_header, data=data, verify=self.verify)
        resp.raise_for_status()
        print(resp.status_code)
        return resp.json()

