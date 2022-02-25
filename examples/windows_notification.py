from veeam_easy_connect import VeeamEasyConnect
from win10toast import ToastNotifier
import getpass
import time

"""
Example of a basic Windows Notification app.

Every 30 seconds a call is sent to the API sessions,
if there is a new activity ID that doesn't match last previously stored item, it is stopped, and it is Failed.
It will then show a Windows Alert.

Requires win10toast > pip install win10toast

"""

def main():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    address = input("Enter address: ")
    ses_url = "sessions?limit=10"
    vec = VeeamEasyConnect(username, password, False)
    vec.vbr().login(address)
    toaster = ToastNotifier()
    res = vec.get(ses_url, False)
    data = res['data'][0]

    try:
        while True:
            time.sleep(30)
            res2 = vec.get(ses_url, False)
            data2 = res2['data'][0]
            if data['activityId'] != data2['activityId']:
                if data2['state'] == "Stopped":
                    if data2['result']['result'] == "Failed":
                        string = f"Alert! Job: {data2['name']} failed!"
                        toaster.show_toast("Alert!", string, threaded=True, icon_path="veeam.ico", duration=3)
            else:
                toaster.show_toast("Notification", "All is fine", threaded=True, icon_path="veeam.ico", duration=3)
            data = data2
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()