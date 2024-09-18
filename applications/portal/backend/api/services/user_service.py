import jwt
from cloudharness.middleware import get_authentication_token
from api.services.keycloak_service import KeycloakService


class UnrecognizedUser(Exception):
    pass


def get_current_user_id() -> str:

    try:
        token = get_authentication_token().replace("Bearer ", "")
        return jwt.decode(token, options={"verify_signature": False}, algorithms='RS256')['sub']
    except Exception as e:
        raise UnrecognizedUser()


def check_if_user_is_admin():
    """
    Function that is used to validate the token and check if the user is an admin
    """
    auth = KeycloakService()
    if auth.current_user_has_realm_role("administrator"):
        return True
    raise Exception("User is not an admin")
