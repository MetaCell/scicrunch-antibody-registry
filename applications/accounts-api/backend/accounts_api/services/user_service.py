from datetime import datetime
from keycloak.exceptions import KeycloakGetError, KeycloakError
from keycloak import KeycloakOpenID
from accounts_api.models import User
from cloudharness.auth import AuthClient, get_server_url, get_auth_realm
from cloudharness import log
from cloudharness.applications import get_configuration
import typing
import re

# from cloudharness.models import User as CHUser # Cloudharness 2.0.0

accounts_app = get_configuration('accounts')


class UserNotFound(Exception):
    pass


class UserNotAuthorized(Exception):
    pass

class ValidationError(Exception):
    pass

def get_user(userid: str) -> User:
    try:
        client = AuthClient()
        kc_user = client.get_user(userid)
    except KeycloakGetError as e:
        if e.response_code == 404:
            raise UserNotFound(userid)
        raise Exception("Unhandled Keycloak exception") from e
    except KeycloakError as e:
        raise Exception("Unhandled Keycloak exception") from e

    user = map_user(kc_user)
    try:
        current_user = client.get_current_user()
        if not current_user or current_user['id'] != userid:
            user.email = None
    except:  # user not provided
        log.error("Error checking user", exc_info=True)
        user.email = None
    return user


def get_users(query: str) -> typing.List[User]:
    try:
        client = AuthClient()
        kc_users = client.get_users(query)
    except KeycloakError as e:
        raise Exception("Unhandled Keycloak exception") from e
    all_users = []
    for kc_user in kc_users:
        auser = map_user(kc_user)
        auser.email = None  # strip out the e-mail address
        all_users.append(auser)

    return all_users


def map_user(kc_user) -> User:
    user = kc_user if isinstance(
        kc_user, dict) else User.from_dict(kc_user._raw_dict)
    if 'attributes' not in kc_user or not kc_user['attributes']:
        kc_user['attributes'] = {}

    user.profiles = {k[len('profile--')::]: kc_user['attributes'][k][0]
                     for k in kc_user['attributes'] if kc_user['attributes'][k] and len(k) > len('profile--') and k.startswith('profile--')}
    try:
        user.avatar = kc_user['attributes'].get('avatar', [None])[0]
    except (IndexError, TypeError):
        # no avatar is set or is empty
        pass

    try:
        user.website = kc_user['attributes'].get('website', [None])[0]
    except (IndexError, TypeError):
        # no website is set or is empty
        pass

    try:
        user.orcid = kc_user['attributes'].get('orcid', [None])[0]
    except (IndexError, TypeError):
        # no website is set or is empty
        pass

    if 'userGroups' in kc_user:
        user.groups = [g['name'] for g in kc_user['userGroups']]
    return user


def update_user(userid, user: User):
    client = AuthClient()

    try:
        current_user = client.get_current_user()
        if current_user['id'] != userid != user.id:
            raise UserNotAuthorized
        admin_client = client.get_admin_client()
        updated_user = {
            'firstName': user.first_name or current_user['firstName'],
            'lastName': user.last_name or current_user['lastName'],
            'username': user.username or current_user['username'],
            'attributes': {
                **(current_user.get('attributes') or {}),
                **({('profile--' + k): user.profiles[k] for k in user.profiles} if user.profiles else {}),
                'avatar': user.avatar,
                'website': user.website,
                'orcid': user.orcid
            }
        }

        admin_client.update_user(userid,  updated_user)
        return get_user(userid)
    except KeycloakError as e:
        if e.response_code == 404:
            raise UserNotFound(userid)
        raise Exception("Unhandled Keycloak exception") from e


def validate_password(username: str, old_password: str):
    keycloak_openid = KeycloakOpenID(server_url=get_server_url(),
                                     client_id=accounts_app.webclient.id,
                                     realm_name=get_auth_realm(),
                                     client_secret_key=accounts_app.webclient.secret)
    try:
        keycloak_openid.token(username, old_password)
    except KeycloakError as e:
        if e.response_code == 401:
            raise UserNotAuthorized()
        raise Exception("Unhandled Keycloak exception") from e


def update_password(username: str, new_password: str):
    client = AuthClient()
    admin_client = client.get_admin_client()
    try:
        admin_client.set_user_password(
            admin_client.get_user_id(username=username),
            new_password, temporary=False
        )
    except KeycloakError as e:
        raise Exception(
            "Unhandled Keycloak exception while updating user") from e

def associate_orcid_id(userid: str, orcid: str):
    client = AuthClient()
    admin_client = client.get_admin_client()
    try:
        orcid_no_prefix = orcid.replace("https://orcid.org/", "")

        admin_client.update_user(userid,  {"attributes": {"orcid": orcid}})
        admin_client.add_user_social_login(userid, "orcid", orcid_no_prefix, orcid_no_prefix)
    except KeycloakError as e:
        try:
            admin_client.delete_user_social_login(userid, "orcid")
            admin_client.add_user_social_login(userid, "orcid", orcid_no_prefix, orcid_no_prefix)
        except KeycloakError as e:
            raise Exception(
                "Unhandled Keycloak exception while updating user") from e

def validate_orcid_id( orcid: str) -> bool:
    return re.match(r'^https://orcid.org/\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$', orcid)
    