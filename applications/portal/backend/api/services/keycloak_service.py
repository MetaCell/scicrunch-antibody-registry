import logging

from django.contrib.auth.models import User

from api.utilities.decorators import refresh_keycloak_client
from cloudharness.auth import AuthClient


class KeycloakService:
    def __init__(self):
        self.keycloak_admin = AuthClient().get_admin_client()

    @refresh_keycloak_client
    def create_user(self, payload, **kwargs):
        return self.keycloak_admin.create_user(payload, **kwargs)

    @refresh_keycloak_client
    def add_user_social_login(self, user_id, provider_id, provider_user_id, provider_user_name):
        return self.keycloak_admin.add_user_social_login(user_id, provider_id, provider_user_id, provider_user_name)

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