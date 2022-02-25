import requests
from requests.auth import HTTPBasicAuth
from .api_settings import api_settings
import urllib3
urllib3.disable_warnings()
import json
import webbrowser
import sys

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

    def __em_login(self) -> None:
        self.basic = True
        self.basic_headers = {
            "accept": "application/json",
        }

        # self.basic_url = f"https://{address}:9398/api/sessionMngr/?v=latest"
        self.basic_url = f"https://{self.address}{self.url_end}"
        self.b_auth = HTTPBasicAuth(self.username, self.password)
        self.response = requests.post(
            self.basic_url, headers=self.basic_headers, auth=self.b_auth, verify=self.verify)
        self.response.raise_for_status()
        self.basic_id = self.response.headers["X-RestSvcSessionId"]
        self.res_json_basic = self.response.json()
        self.reqest_header = self.get_request_header()

    def login(self, address: str) -> None:
        if self.basic:
            self.address = address
            self.__em_login()
        else:
            # set up each login url endpoint and api version
            self.address = address
            self.oauth_url = f"https://{self.address}{self.url_end}"
            self.oauth_data = {"grant_type": "password",
                               "username": self.username,
                               "password": self.password}
            self.response = requests.post(
                self.oauth_url, data=self.oauth_data, headers=self.oauth_headers, verify=self.verify)
            self.response.raise_for_status()
            self.res_json_oauth = self.response.json()
            if "mfa_token" not in self.res_json_oauth:
                self.reqest_header = self.get_request_header()
            else:
                print(
                    f"MFA Token in response - use 'mfa_token_login' to with access code to continue")

    def mfa_token_login(self, code: str) -> None:
        self.token = self.res_json_oauth['mfa_token']
        self.mfa_url = f"https://{self.address}{self.url_end}"
        self.mfa_data = {
            "grant_type": "Mfa",
            "mfa_token": self.token,
            "mfa_code": code
        }
        # I don't think I need to change the Content-Type on this request- not clear

        self.response = requests.post(
            self.mfa_url, data=self.mfa_data, headers=self.oauth_headers, verify=self.verify)
        self.response.raise_for_status()
        self.res_json_oauth = self.response.json()
        self.reqest_header = self.get_request_header()

    def save_token(self, file_name: str) -> None:
        # Added a check in case extension was included
        file_name = file_name.split(".")[0] if "." in file_name else file_name

        if self.basic:
            data = self.response.headers
        else:
            data = self.res_json_oauth
        with open(f"{file_name}.json", "w") as token_file:
            json.dump(dict(data), token_file)

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
        if self.basic:
            headers = {
                "accept": "application/json",
                "X-RestSvcSessionId": self.basic_id
            }
        else:
            headers = self.api_settings[self.api_type]['headers']
            # need to add application/json here?
            if "application/x-www-form-urlencoded" in headers.values():
                headers.pop('Content-type')
            bearer_string = 'Bearer ' + self.res_json_oauth['access_token']
            headers['Authorization'] = bearer_string
        return headers

    def save_request_header(self, file_name: str) -> None:
        file_name = file_name.split(
            ".")[0] + ".json" if "." in file_name else file_name + ".json"
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
        self.api_settings = api_settings
        # with open("api_settings.json", "r") as settings_file:
        #     self.api_settings = json.load(settings_file)

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
        self.update_settings("ent_man")
        # self.api_type = "ent_man"
        return self
    # Update the URL and headers as needed

    def update_settings(self, api_type: str) -> None:
        if api_type == "o365":
            self.url_end = self.api_settings['o365']['url']
            self.api_version = self.api_settings['o365']['api_version']
            # No API version specified in the documentation
        elif api_type == "aws":
            self.url_end = self.api_settings['aws']['url']
            self.oauth_headers = self.api_settings['aws']['headers']
            self.api_version = self.api_settings['aws']['api_version']
        elif api_type == "vbr":
            self.url_end = self.api_settings['vbr']['url']
            self.oauth_headers = self.api_settings['vbr']['headers']
            self.api_version = self.api_settings['vbr']['api_version']
        elif api_type == "azure":
            self.url_end = self.api_settings['azure']['url']
            self.oauth_headers = self.api_settings['azure']['headers']
            self.api_version = self.api_settings['azure']['api_version']
        elif api_type == "gcp":
            self.url_end = self.api_settings['gcp']['url']
            self.oauth_headers = self.api_settings['gcp']['headers']
            self.api_version = self.api_settings['gcp']['api_version']
        elif api_type == "ent_man":
            self.url_end = self.api_settings['ent_man']['url']
            self.api_version = "None"
        else:
            print("API type not found")
            return

    def _create_url(self, request: str, full: bool):
        if not full:
            if request.startswith("/"):
                request = request[1:]
            if self.basic:
                # ":9398/api/sessionMngr/?v=latest"
                url_middle = "/".join(self.url_end.split("/")[:-2]) + "/"
                # the beginning / has been removed from the request variable
                # No api_version needs to be added in this case
                return f"https://{self.address}{url_middle}{request}"
            else:
                #":11005/api/v1/token"
                # check if oauth is in the url_end as that means we need to go back 
                # two splits unlike the others that need 1
                split_qty = -2 if "oauth" in self.url_end else -1
                url_middle = "/".join(self.url_end.split("/")[:split_qty]) + "/"
                # the beginning / has been removed from the request variable
                # But the api_version doesn't have the trailing / so needs to be added
                return f"https://{self.address}{url_middle}{self.api_version}/{request}"
        else:
            return request

    def get(self, url: str, full=True) -> dict:
        url = self._create_url(url, full)
        resp = requests.get(
            url, headers=self.reqest_header, verify=self.verify)
        resp.raise_for_status()
        return resp.json()

    def post(self, url: str, data: dict, full=True) -> dict:
        url = self._create_url(url, full)
        resp = requests.post(url, headers=self.reqest_header,
                             data=data, verify=self.verify)
        resp.raise_for_status()
        return resp.json()

    def put(self, url: str, data: dict, full=True) -> dict:
        url = self._create_url(url, full)
        resp = requests.put(url, headers=self.reqest_header,
                            data=data, verify=self.verify)
        resp.raise_for_status()
        return resp.json()

    def update_port(self, port_num: str) -> None:
        end_bit = self.url_end.split("/", maxsplit=1)[1]
        self.url_end = f":{port_num}/{end_bit}"

    def get_port(self) -> str:
        return self.url_end.split("/", maxsplit=1)[0][1:]

    def update_api_version(self, api_version: str) -> None:
        if not self.basic:
            self.oauth_headers['x-api-version'] = api_version

    def get_api_version(self) -> None:
        if not self.basic:
            return self.oauth_headers['x-api-version']
        else:
            return "latest"

    # being worked on
    def __sso_login(self, address: str, sso_username: str, sso_address: str):
        # set up for first request

        # remove the /token from the url_end brought in from config file
        sso_url = "/".join(self.url_end.split("/")
                           [0:3]) + "/identityProvider/signOnUrl?userName="

        # create the full url
        url = f"https://{address}:{sso_url}{sso_username}"
        api_version = self.oauth_headers.get("x-api-version")
        headers = {"x-api-version": api_version}

        # send first request
        data = requests.get(url, headers=headers, verify=self.verify)
        data.raise_for_status()
        data_json = data.json()

        # confirm SSO
        sso_url = data_json.get("redirectToUrl")
        print("opening webpage")
        webbrowser.open(sso_url)
        confirm = input("continue? y/n")
        if confirm == "n":
            sys.exit()

        # second request set up
        data = {
            "username": self.username,
            "password": self.password
        }
        headers['Content-Type'] = "x-www-form-urlencoded"

        # get the code from the response to add to the new url
        saml_code = sso_url.split("=")[1]
        saml_url = f"https://{sso_address}//adfs/ls/?SAMLRequest={saml_code}"

        # send third request

        saml_res = requests.post(
            saml_url, data=data, headers=headers, verify=self.verify)
        saml_res.raise_for_status()

        # third request set up
        token = saml_res.json().get("value")

        login_url = f"https://{sso_address}:11005/api/v1/identityProvider/token"

        headers.pop("Content-Type")
        token_data = {"SamlResponse": token}

        # send third request
        self.respose = requests.post(
            login_url, headers=headers, data=token_data, verify=self.verify)
        self.response.raise_for_status()

        # if all has gone well, set the data as normal
        self.res_json_oauth = self.response.json()
        self.reqest_header = self.get_request_header()
