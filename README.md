# Veeam Easy Connect
## Still under active development, please check back for updates

If you find any bugs please raise an issue

Veeam Easy Connect is a Python module that makes it easier to get going with Veeam APIs.

This module provides an easy way to get Authorized, and get the access token so you can get on with making useful requests.

### Change log

* Added Veeam ONE API support
* Bumped the Veeam Backup for Microsoft 365 to v6
* Fixed issue with API version update command

**Note: I have updated this module so make it more generic over all Veeam Products. This means breaking changes to the way it was shown in the YouTube series.**

Password login should work on:
* Veeam API
* Enterprise Manager (basic auth)
* AWS
* Azure
* GCP
* O365
* VONE

### MFA

AWS and Azure MFA tested and working.

GCP still to be tested but should work.

### AWS SSO

SSO for AWS is in the module but still being worked on.

### Items Not road mapped

O365 Modern App-Only Authentication is intended for Tenant access so is very restricted so is not currently planned.

Authorization code access is not currently road mapped.

**Happy to have more people working on this so pull requests are welcome!**

## Installation

Install has now moved to Pypi!

    pip install veeam_easy_connect

## Update

    pip install --upgrade veeam_easy_connect

## How to use

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
* .vone

Then chain with the .login() command with the address

    address = "192.168.0.123"

    vec.aws().login(address) 

    token = vec.get_access_token()

### Custom api type

To create a custom API type (oauth only) do the following.

Create a dictionary with the following parameters, obviously modifying what you need to:

    settings = {
                "headers": {
                    "accept": "application/json",
                    "Content-type": "application/x-www-form-urlencoded",
                    "x-api-version": "1.0-rev2"
                },
                "url": ":1239/api/token",
                "api_version": "v1"
            }

The url is the token endpoint with the port included, and the app version has to be the same one that is used when making a regular http request e.g. v1/2/3

Then call the following function with the settings as the parameter.

    vec.custom(settings)

You can then carry on like normal.
## MFA Authentication

AWS and Azure currently (GCP soon)
    
    vec = VeeamEasyConnect(username, password)

    vec.aws().login(address) # or .azure()

    res_code = input("Enter MFA code: ")

    vec.mfa_login(res_code) # string, no need to set the api type again

## Request Methods

You can send requests directly using vec methods which wrap the Request library and pulls in the correct headers automatically. 

This can be useful for single use scripts or when using Jupyter Notebooks.

    address = f"https://192.168.0.123:9419/api/v1/backupInfrastructure/repositories"

    res_data = vec.get(address) -> dict

    res_data = vec.post(address, body_data) -> dict

    res_data = vec.put(address, body_data) -> dict

All of these methods return a deserialized response. 

## Short Request URLs

To save some effort you can specify just the last part of the URL without the version number on APIs that
use it for example:

"https://192.168.0.123:9419/api/v1/backupInfrastructure/repositories"

Can be shortened to:

"backupInfrastructure/repositories"

    address = "backupInfrastructure/repositories"
    res_data = vec.get(address, False)
    # or
    res_data = vec.get(address, full=False)

You need to pass "False" as the last or named parameter, which stands for "not full url".
## Get Request Header

You can get the complete header by calling:

    req_header = vec.get_request_header()

The request will include the correct API version for the type of API you are using. 

To save the headers to a JSON file:

    vec.save_request_header("file_name")

## Get Access Token

To get just the token you can call one of the following:

    token = vec.get_access_token()
    or 
    token = vec.get_access_token_with_bearer() # adds the "Bearer " to the token (oauth)

This will grab the mfa_token from the oauth response and combine it in the code you enter into the correct body. 

To save the access token data to a JSON file use:

    vec.save_token("file_name")

## Update port

To update the port you need to do the following:

    vec.vbr()

    vec.update_port("9420")

    print(vec.get_port()) # check the port has changed

    vec.login("address")

## Update API Version

    # set the API type
    vec.vbr().update_api_version("1.0-rev3")
    
    # check
    print(vec.get_api_version())

Note that you cannot chain the api and port updates, you would need to do:

    # set the API type
    vec.vbr().update_api_version("1.0-rev3")

    # Then update the port or visa-versa
    vec.update_port("9420")

## Examples

Please see examples of using vec in the examples folder.

## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam Backup and Replication API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)
