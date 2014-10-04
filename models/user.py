class User(object):
    def __init__(self, access_token=None):
        self.Token = access_token

    def is_authenticated(self):
        return self.Token is not None and self.Token.is_valid()
