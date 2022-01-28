from hashlib import pbkdf2_hmac


class PasswordHash:
    def __init__(self, password: str, salt: str):
        self.salt = salt
        self.password = password

    def get_hex(self):
        return pbkdf2_hmac('sha512', self.password.encode('utf8'), self.salt.encode('utf8'), 3).hex()
