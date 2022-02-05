# Veeam Easy Connect
## Still under active development, please check back for updates

If you find any bugs please raise an issue

Veeam Easy Connect is a Python module that makes it easier to get going with Veeam APIs.

This module provides an easy way to get Authorized, and get the access token so you can get on with making useful requests.

**Note: I have updated this module so make it more generic over all Veeam Products. This means breaking changes to the way it was shown in the YouTube series.**

Password login should work on:
* Veeam API
* Enterprise Manager (basic auth)
* AWS
* Azure
* GCP
* O365

MFA Login AWS and Azure are new and still need testing - help here welcome. 

GCP MFA is being worked on as different to the way AWS and Azure work.

SSO for AWS is not currently implemented, but being looked into.

O365 Modern App-Only Authentication is intended for Tenant access so is very restricted so is not currently planned.

Authorization code access is not currently road mapped.

**Happy to have more people working on this so pull requests are welcome!**

## Installation

    pip install -r requirements.txt

External Packages used:

* Requests

## How to use

There is a new api_settings file with all the variations on the headers and url paths loaded. I've done this to make it easier to update if the API or URLs change. If you are using a none-standard port you will need to update this file.

Import the module via:

    from veeam_easy_connect import VeeamEasyConnect

Next you need to create an instance of the object with your username and password.

    username = "john@abc.com"

    password = "super_secret"

    vec = VeeamEasyConnect(username, password, True) # secure - checks SSL - bool is optional 

    vec = VeeamEasyConnect(username, password, False) # insecure - if you are using a Self-Signed Cert (not recommended)

## Password Authentication

Next call the api type which is either: 
* .ent_man - enterprise manager 
* .aws
* .azure
* .gcp
* .vbr
* .o365

Then chain with the .login() command with the address

    address = "192.168.0.123"

    vec.aws().login(address) 

    token = vec.get_access_token()

## MFA Authentication

AWS and Azure only. 

This still is being tested, please create issue if you find a bug.
    
    vec = VeeamEasyConnect(username, password)

    vec.aws().login(address) # or .azure()

    vec.get_mfa_token() # this will print the token to use with the MFA

    res_code = input("Enter code: ")

    vec.mfa_login(res_code) # string, no need to set the api type again

## Request Methods

You can send requests directly using vec methods which wrap the Request library and pulls in the correct headers automatically.

    address = f"https://192.168.0.123:9419/api/v1/backupInfrastructure/repositories"

    res_data = vec.get(address) -> dict

    res_data = vec.post(address, body_data) -> dict

    res_data = vec.put(address, body_data) -> dict

All of these methods return a deserialised response. No delete method is available and is not planned.

## Get Request Header

You can get the complete header by calling:

    req_header = vec.get_request_header()

The request will include the correct API version for the type of API you are using. 

To save the headers to a JSON file:

    vec.save_headers("file_name")

## Get Access Token

To get just the token you can call one of the following:

    token = vec.get_access_token()
    or 
    token = vec.get_access_token_with_bearer() # adds the "Bearer " to the token (oauth)

This will grab the mfa_token from the oauth response and combine it in the code you enter into the correct body. 

To save the access token data to a JSON file use:

    vec.save_token("file_name")

## Examples

Please see examples of using vec in the examples folder.

## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam Backup and Replication API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)
