import requests
from requests.exceptions import RequestException

DEFAULT_HEADERS = {
    "User-Agent": "SimpleWebVulnScanner/1.0"
}

TIMEOUT = 8


def get(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=DEFAULT_HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        return response
    except RequestException as e:
        print(f"[ERROR] GET request failed for {url}: {e}")
        return None


def post(url, data=None):
    try:
        response = requests.post(
            url,
            data=data,
            headers=DEFAULT_HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        return response
    except RequestException as e:
        print(f"[ERROR] POST request failed for {url}: {e}")
        return None