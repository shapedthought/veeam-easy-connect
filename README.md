# Veeam Easy Connect

Veeam Easy Connect is a Python module that makes it easier to get going with both the Veeam Enterprise Manager API as well as the newer V11 API.

The aim is to make a bit easier to connect to either API and get the access token so you can start making data requests.

## Installation

    pip install -r requirements.txt

External Packages used:

* Requests

## How to use

Import the module via:

    from veeam_easy_connect import VeeamEasyConnect

Next you need to create an instance of the object

    veeam_ec = VeeamEasyConnect

Now you can log into either Enterprise Manager or V11 APIs

Enterprise Manager:

    em_headers = veeam_ec.em_login()

V11:

    v11_headers = veeam_ec.v11_login()

Both of these will prompt you for log in each time you run the module. 

If you want to save the headers so you can load and re-use them later, saving on th amount of 
logins you do, I recommend doing the following. 

Create save and load functions:

    import json
    def save_json(headers_file_name, headers_data):
        with open(headers_file_name, "w") as headers_file:
            json.dump(headers_data, headers_file)

    def read_json(headers_file_name):
        with open(headers_file_name, "r") as headers_file:
        headers = json.load(headers_file)

You can then call them like so:

    # save
    save_json("headers.json", headers_data)

    # load
    headers= read_json("headers.json")

You can then use those headers until the token runs out.
## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam V11 API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)