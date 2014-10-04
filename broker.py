import urllib
import json
import requests
from models.access_token import AccessToken


class Broker(object):
    authorize_url = "https://api.home.nest.com/oauth2/access_token"
    base_url = "https://developer-api.nest.com"

    def _get_client_data(self, code=None):
        client_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code"
        }
        if code:
            client_data.update(code=code)
        return urllib.urlencode(client_data)

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _make_request(self, url, method="GET", data={}, headers={}):
        response = None
        if method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, data=data, headers=headers)
        else:
            raise Exception("Only GET/POST is supported.")

        response.raise_for_status()
        return response

    def request_access_token(self, pincode):
        request_data = self._get_client_data(pincode)
        response = self._make_request(self.authorize_url, "POST", request_data)
        content = response.json()
        return AccessToken(content.access_token, content.expires_in, pincode=pincode)

    def request(self, access_token="", body=None, headers=None):
        headers = headers or {}
        body = body or {}
        if not "auth" in body:
            body.update(auth=access_token)

        url = self.base_url + "/devices"
        response = self._make_request(url, "GET", body, headers) 
        return response


class NestAccessTokenError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
