import jwt
from cloudharness.middleware import get_authentication_token

class UnrecognizedUser(Exception):
    pass

def get_current_user_id() -> str:
    token = get_authentication_token()
    try:
        return jwt.decode(token, options={"verify_signature": False}, algorithms='RS256')['sub']
    except Exception as e:
        raise UnrecognizedUser()