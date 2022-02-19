api_settings = {
    "o365": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
        },
        "url": ":4443/v5/Token"
    },
    "aws": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.2-rev0"
        },
        "url": ":11005/api/v1/token"
    },
    "vbr": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.0-rev2"
        },
        "url": ":9419/api/oauth2/token"
    },
    "azure": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
        },
        "url": "/api/oauth2/token"
    },
    "gcp": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.0-rev0"
        },
        "url": ":13140/api/v1/token"
    }
}