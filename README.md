# Veeam Easy Connect
## Still under active development, please check back for updates

If you find any bugs please raise an issue

Veeam Easy Connect is a Python module that makes it easier to get going with both the Veeam APIs.

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

    vec = VeeamEasyConnect(username, password, False) # insecure - if you are using Self-Signed Cert (not recommended)

## Password Authentication

Next call the api type which is either: 
* .ent_man() - enterprise manager 
* .aws()
* .azure()
* .gcp()
* .vbr()
* .o365()

You then chain with the .login() command with the address

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

    token = vec.get_access_token()
    or 
    token = vec.get_access_token_with_bearer() # adds the "Bearer " to the token

This will grab the mfa_token from the oauth response and combine it in the code you enter into the correct body.

If Authorization was successful in all cases you will see an "OK" printed.

As you will likely need to save the token for later use a convenience method has been added:

    vec.save_data("tokendata")

Just add the name of the file you want, without an extension, VEC will do the rest.

## Examples

The examples folder has scripts showing authentication process and saving the token in a JSON file for future use. 

There is also a script that shows how to then use the token in a request and save the response in a JSON file.

## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam V11 API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)