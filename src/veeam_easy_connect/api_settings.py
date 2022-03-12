api_settings = {
    "o365": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
        },
        "url": ":4443/v6/Token",
        "api_version": "v6"
    },
    "aws": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.2-rev0"
        },
        "url": ":11005/api/v1/token",
        "api_version": "v1"
    },
    "ent_man": {
        "url": ":9398/api/sessionMngr/?v=latest"
    },
    "vbr": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.0-rev2"
        },
        "url": ":9419/api/oauth2/token",
        "api_version": "v1"
    },
    "azure": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded"
        },
        "url": "/api/oauth2/token",
        "api_version": "v3"
    },
    "gcp": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.0-rev0"
        },
        "url": ":13140/api/v1/token",
        "api_version": "v1"
    },
    "vone": {
        "headers": {
            "accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "x-api-version": "1.0-rev2"
        },
        "url": ":1239/api/token",
        "api_version": "v2"
    },
}