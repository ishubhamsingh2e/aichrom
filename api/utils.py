import jwt
from django.conf import settings


def generate_jwt(phone):
    payload = {'phone': phone}
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token


def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return True, payload['phone']
    except jwt.ExpiredSignatureError:
        return False, None  # Token has expired
    except jwt.InvalidTokenError:
        return False, None  # Invalid token
