import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
import getpass
import json


class VeeamEasyConnect():
    def __init__(self) -> None:
        self.em_port = 9398
        self.v11_port = 9419
        self.v11_headers = {"accept": "application/json",
                                    "x-api-version": "1.0-rev1", "Content-Type": "application/x-www-form-urlencoded"}
        self.v11_token_headers = {"accept": "application/json", "x-api-version": "1.0-rev1"} 
        self.em_headers = {"Accept": "application/json"}

    def em_login(self) -> list[dict]:
        self.address = input("Enterprise Manager IP: ")
        self.username = input("Username: ")
        self.password = getpass.getpass("Password: ")
        self.login_url = f"https://{self.address}:{self.em_port}/api/sessionMngr/?v=v1_6"
        auth=HTTPBasicAuth(self.username, self.password)
        res = requests.post(self.login_url, auth=auth, verify=False)
        res.raise_for_status()
        self.em_token = res.headers.get('X-RestSvcSessionId')
        self.em_headers['X-RestSvcSessionId'] = self.em_token
        return self.em_headers

    def v11_login(self) -> list[dict]:
        self.v11_address = input("V11 API IP: ")
        self.v11_username = input("Username: ")
        self.v11_password = getpass.getpass("Password: ")

        self.v11_data = {"grant_type" : "password", "username" : self.v11_username, "password": self.v11_password}
        self.v11_login_url = f"https://{self.v11_address}:{self.v11_port}/api/oauth2/token"
        v11_res = requests.post(self.v11_login_url, data=self.v11_data, headers=self.v11_headers, verify=False)
        v11_res.raise_for_status()
        self.v11_res_json = v11_res.json()
        self.v11_status_code = v11_res.status_code
        self.v11_token = self.v11_res_json.get('access_token')
        self.v11_token_headers['Authorization'] = 'Bearer ' + self.v11_token
        return self.v11_token_headers

    def save_headers(self, headers: list[dict], name: str) -> None:
        with open(name, "w") as headers_file:
            json.dump(headers, headers_file)

    
    def load_headers(self, file_name: str) -> dict:
        if ".json" in file_name:
            file_name = file_name.split(".")[0]
        with open(f"{file_name}.json", "r") as headers_file:
            json_data = json.load(file_name)
        return json_data

    