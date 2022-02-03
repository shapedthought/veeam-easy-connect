# Veeam Easy Connect

Veeam Easy Connect is a Python module that makes it easier to get going with both the Veeam APIs.

This module provides an easy way to get Authorized, and get the access token so you can get on with making useful requests.

**Note**

I have updated this module so make it more generic over all Veeam Products. This means breaking changes to the way it was shown in the YouTube series.

## Installation

    pip install -r requirements.txt

External Packages used:

* Requests

## How to use

Import the module via:

    from veeam_easy_connect import VeeamEasyConnect

Next you need to create an instance of the object with your username and password.

    veeam_ec = VeeamEasyConnect(username, password)

Now you can log login with Basic Auth or OAuth:

Basic Auth (Enterprise Manager):

    veeam_ec.basic_auth(address)

OAuth:

    veeam_ec.oauth(address)

You only need to supply the address of the URL, not the full string e.g. "192.168.0.123", not "https://192.168.0.123:9398"

You will note that there is no response from either of these, but you can get the json responses by calling:

    json_data = veeam_ec.get_json("basic") 
    json_data = veeam_ec.get_json("oauth")

As you will likely need to save the token for later use a convenience method has been added:

    veeam_ec.save_data("oauth", "tokendata")

The first parameter is type of token data ("oauth" or "basic"), and the second is the name of the file you require. 

The examples folder has a script showing authentication process and saving the token. There is also a script that
shows how to then use the token in the saved json file.

## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam V11 API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)