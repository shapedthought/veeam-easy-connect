from veeam_easy_connect import VeeamEasyConnect
import sys
import pprint

"""
Example of a script where you pass in arguments and
it sends back data (get only).

Example:
python get_vbr_with_args.py username password url 
"""

def main():
    username = sys.argv[1]
    password = sys.argv[2]
    url = sys.argv[3]

    vec = VeeamEasyConnect(username, password, False) # Insecure

    # extracts just the address from the url to allow for login
    address = url.split("//")[1].split(":")[0]

    vec.vbr().login(address)
    res = vec.get(url)
    pprint.pprint(res)


if __name__ == "__main__":
    main()