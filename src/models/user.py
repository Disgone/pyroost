class User(object):
    def __init__(self, access_token=None):
        self.token = access_token

    def is_authenticated(self):
        return self.token is not None and self.token.is_valid()