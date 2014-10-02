import urllib
from httplib2 import Http
import simplejson
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
        http = Http(disable_ssl_certificate_validation=True)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = http.request(self.authorize_url, "POST", body=request_data, headers=headers)
        reply = simplejson.loads(content)

        if response['status'] != "200":
            if "error_description" in reply:
                raise NestAccessTokenError("Access token error: %s" % reply["error_description"])
            else:
                raise NestAccessTokenError("The server returned a non-successful response %s" % self.authorize_url)

        return AccessToken(reply["access_token"], reply["expires_in"], pincode=pincode)


class NestAccessTokenError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description