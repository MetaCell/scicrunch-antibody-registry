import jwt
from cloudharness.middleware import get_authentication_token
from api.services.keycloak_service import KeycloakService
from api.utilities.cache import ttl_cache


class UnrecognizedUser(Exception):
    pass


def get_current_user_id() -> str:

    try:
        token = get_authentication_token().replace("Bearer ", "")
        return jwt.decode(token, options={"verify_signature": False}, algorithms='RS256')['sub']
    except Exception as e:
        raise UnrecognizedUser()


@ttl_cache(maxsize=2048, ttl=60)
def _user_pk_by_kc_id(kc_id):
    from cloudharness_django.services.user import get_user_by_kc_id
    user = get_user_by_kc_id(kc_id)
    return user.pk if user else None


def get_current_user_pk():
    """Django User pk of the JWT caller, or None."""
    try:
        return _user_pk_by_kc_id(get_current_user_id())
    except UnrecognizedUser:
        return None


def check_if_user_is_admin():
    """
    Function that is used to validate the token and check if the user is an admin
    """
    auth = KeycloakService()
    if auth.current_user_has_realm_role("administrator"):
        return True
    raise Exception("User is not an admin")
