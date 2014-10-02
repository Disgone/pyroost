import shelve
from models.user import User
from broker import *


class RoostClient(object):
    def __init__(self, client_id, client_secret):
        self.Name = "Roost"
        self.User = User()
        self.client_id = client_id
        self.client_secret = client_secret
        self._load_state()

    def _load_state(self):
        settings = shelve.open("roost.settings")
        print settings
        if "user" in settings:
            self.User = settings["user"]
        settings.close()

    def _save_state(self):
        settings = shelve.open("roost.settings")
        settings["user"] = self.User
        settings.close()

    def login(self, pincode):
        broker = Broker(self.client_id, self.client_secret)
        try:
            token = broker.request_access_token(pincode)
            self.User = User(token)
            self._save_state()
        except NestAccessTokenError as token_error:
            print ("Access Token Error: %s" % token_error.description)