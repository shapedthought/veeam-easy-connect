from email.policy import default
from veeam_easy_connect import VeeamEasyConnect
import json
import click

"""
Example of a basic CLI programme using the Click library. 

Uses the short request URL version, see README

Requires click > pip install click

Options:
* address = server address
* url = end of the url
* type = API Type
* username = username for API
* password = password for API
* verify = use SSL, default true
* file = filename for JSON output
* help = see the help output

Example:

python click_cli.py \
    --address "192.168.0.123" \
    --url "objectRestorePoints" \
    --type "GET" \
    --username "administrator@veeam.com" \
    --password "your_password" \
    --verify false \
    --file "object_points"
"""

@click.command()
@click.option('--address', help="API Address")
@click.option('--url', help="End url of API call")
@click.option('--data', help="Data for POST and PUT")
@click.option('--type', default="GET", help="Request type")
@click.option('--file', help="file name")
@click.option('--username', help="API username")
@click.option('--password', help="API password, default is true")
@click.option('--verify', default=True, help="SSL check")
def main(address, url, data, type, file, username, password, verify):

    vec = VeeamEasyConnect(username, password, verify)
    vec.vbr().login(address)

    match type:
        case "GET":
            data = vec.get(url, False)
        case "POST":
            data = vec.post(url, data, False)
        case "PUT":
            data = vec.post(url, data, False)

    with open(f"{file}.json", "w") as jd:
        json.dump(data, jd)

if __name__ == "__main__":
    main()