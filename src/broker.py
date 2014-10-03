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

    def request_access_token(self, pincode):
        request_data = self._get_client_data(pincode)
        response = requests.post(self.authorize_url, data=request_data)

        content = response.json()        
        if response.status_code != requests.codes.ok:
            if "error_description" in content:
                raise NestAccessTokenError("Access token error: %s" % content.error_description)
            else:
                raise NestAccessTokenError("The server returned a non-successful response %s" % self.authorize_url)

        return AccessToken(content.access_token, content.expires_in, pincode=pincode)

    def request(self, access_token="", body=None, headers=None):
        headers = headers or {}
        body = body or {}
        if not "auth" in body:
            body.update(auth=access_token)
        
        r = requests.get(self.base_url + "/devices", params=body, headers=headers)
        return r


class NestAccessTokenError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
