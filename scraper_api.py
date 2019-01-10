import requests
import json

# Must be set after importing
URL = None
KEY = None


class ScraperApiException(Exception):
    def __init__(self, message):
        self.message = message


def upload_target_url(target_url, pool='public'):
    """
    API call for uploading the target URL to the server

    """
    headers = {'Authorization': 'Token ' + str(KEY), 'Content-type': 'application/json'}
    payload = {
        "url": target_url,
        "pool": pool,
    }
    resp = requests.post(URL + 'urls/', data=json.dumps(payload), headers=headers)
    if resp.status_code == 201:
        return resp.json()
    else:
        raise ScraperApiException(resp.json()['detail'])


def get_scrap_result(scrap_id):
    """
    API call to get scrap result

    """
    headers = {'Authorization': 'Token ' + KEY, 'Content-type': 'application/json'}
    resp = requests.get(URL + 'scrapes/' + str(scrap_id) + '/result', headers=headers)
    if resp.status_code == 200:
        return resp.content
    else:
        raise ScraperApiException(resp.json()['detail'])


def get_url_info(url_id):
    """
    API call for checking URL status

    """
    headers = {'Authorization': 'Token ' + KEY, 'Content-type': 'application/json'}
    resp = requests.get(URL + 'urls/' + str(url_id), headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise ScraperApiException(resp.json()['detail'])
