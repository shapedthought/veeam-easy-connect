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

You can then add these headers when you make API requests using the "Requests" library.

    # Enterprise Manager Request
    import Requests

    url = "https://192.168.4.44:9398/api/backupServers"
    
    # headers added here
    res = requests.get(url, headers=em_headers, verify=False) 

    print(res.status_code)

    res_data = res.json()

If you are not using a Jupyter which will cache the VeeamEasyConnect object including the headers or you want to create a Python script which also won't cache the headers between runs, you can do the following. 

    veeam_ec.save_headers(em_headers, "em_headers_file")

That will product a json file with the headers loaded. 

You can then load the headers again, as long as it is within the valid time limit (15 min).

        # Instantiate the class object

        veeam_ec = VeeamEasyConnect

        # Load Headers

        v11_header = veeam_ec.load_headers("em_headers_file.json")

        url = "https://192.168.4.44:9398/api/backupServers"

        res = requests.get(url, headers=em_headers, verify=False) 

        print(res.status_code)

         res_data = res.json()

## Veeam API references

[Enterprise Manager API](https://helpcenter.veeam.com/docs/backup/em_rest/overview.html?ver=110)

[Veeam V11 API](https://helpcenter.veeam.com/docs/backup/vbr_rest/reference/vbr-rest.html?ver=110)