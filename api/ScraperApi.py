import requests
import json


class ScraperApiException(Exception):
    """ Exception class that should be handled where you do api calls """

    def __init__(self, message):
        self.message = message


class ScraperApi:
    URL = 'https://android.scraperclub.com/api/v1/'

    def __init__(self, api_key):
        self.api_key = api_key

    def upload_target_link(self, target_url, pool='waiting'):
        """
        API call for uploading the target URL to the server

        """
        payload = json.dumps({
            "url": target_url,
            "pool": pool,
        })
        resp = requests.post(
            self.URL + 'urls/',
            data=payload,
            headers={'Authorization': 'Token ' + self.api_key, 'Content-type': 'application/json'}
        )
        return self.__handle_response(resp)

    def get_scrap_result(self, scrap_id):
        """
        API call to get scrap result

        """
        resp = requests.get(
            self.URL + 'scrapes/' + str(scrap_id) + '/result',
            headers={'Authorization': 'Token ' + self.api_key}
        )

        return self.__handle_response(resp, False).content

    def get_url_info(self, url_id):
        """
        API call for checking URL status

        """
        resp = requests.get(
            self.URL + 'urls/' + str(url_id),
            headers={'Authorization': 'Token ' + self.api_key}
        )

        return self.__handle_response(resp)

    def get_account_info(self):
        """
        API call for checking account status

        """
        resp = requests.get(
            self.URL + 'info/',
            headers={'Authorization': 'Token ' + self.api_key}
        )

        return self.__handle_response(resp)

    def __handle_response(self, response, json_content=True):
        """
        Method for handling API response
        :return: JSON object if success, or raises exception otherwise

        """
        if 200 <= response.status_code <= 204:
            if json_content:
                return response.json()
            else:
                return response
        else:
            raise ScraperApiException(response.json()['detail'])
