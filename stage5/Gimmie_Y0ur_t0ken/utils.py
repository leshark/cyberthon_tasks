import jwt


class SafeSerializer:
    def __init__(self):
        self.params = {"username": ""}

    def dumps(self, username):
        """:return token"""
        self.params["username"] = username
        encoded_jwt = jwt.encode(self.params, 'qwerty', algorithm='HS256').decode()
        return encoded_jwt

    def loads(self, token):
        """:return user_obj"""
        return jwt.decode(token, 'qwerty', algorithms=['HS256'])


url_serializer = SafeSerializer()
