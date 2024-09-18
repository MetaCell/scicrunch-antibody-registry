import logging
import os

from django.contrib.auth.models import User

from api.utilities.decorators import refresh_keycloak_client
from cloudharness.auth import AuthClient
from cloudharness import log

# Reuse AuthClient to benefit from valid token
# AuthClient will try to refresh automatically once token expired


class KeycloakService:
    def __init__(self, username=None, password=None):
        username = os.getenv("ACCOUNTS_ADMIN_USERNAME", username)
        password = os.getenv("ACCOUNTS_ADMIN_PASSWORD", password)
        self.auth_client = AuthClient(username, password)
        self.keycloak_admin = self.auth_client.get_admin_client()

    @refresh_keycloak_client
    def get_current_userid(self):
        return self.auth_client.get_current_user().get("id", None)

    @refresh_keycloak_client
    def create_user(self, payload, **kwargs):
        return self.keycloak_admin.create_user(payload, **kwargs)

    @refresh_keycloak_client
    def current_user_has_realm_role(self, role):
        return self.auth_client.user_has_realm_role(user_id=self.get_current_userid(), role=role)

    @refresh_keycloak_client
    def add_user_social_login(self, user_id, provider_id, provider_user_id, provider_user_name):
        return self.keycloak_admin.add_user_social_login(user_id, provider_id, provider_user_id, provider_user_name)

    @refresh_keycloak_client
    def get_user_by_username(self, username):
        users = self.auth_client.get_users({"username": username})
        return users[0] if len(users) else None

    @refresh_keycloak_client
    def get_user_by_attribute(self, attribute: str, value: str):
        query = {
            "q": f"{attribute}:{value}"
        }
        users = self.keycloak_admin.get_users(query)
        users_length = len(users)
        try:
            assert users_length < 2
        except AssertionError:
            logging.error(f"There are {users_length} users with {attribute} equal to {value}")
        return users[0] if users_length == 1 else None

    def get_user_id_from_django_user(self, django_user) -> str:
        return self.keycloak_admin.get_user_id(django_user.username)
