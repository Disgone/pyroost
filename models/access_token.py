from datetime import datetime, timedelta


class AccessToken(object):
    def __init__(self, token, expires_in, pincode=None, request_date=None):
        self.token = token
        self.expires_in = expires_in
        self.pincode = pincode

        if request_date is None:
            request_date = datetime.now()
        self.request_date = request_date
        self.token_expiration = self.request_date + timedelta(seconds=self.expires_in)

    def is_valid(self):
        current = datetime.now()
        return current <= self.token_expiration

    def __str__(self):
	return 'AccessToken:%s' % self.token
