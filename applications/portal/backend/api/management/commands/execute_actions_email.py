from django.core.management.base import BaseCommand

from api.management.ingestion.users_ingestor import KeycloakRequiredActions
from api.utilities.decorators import refresh_keycloak_client
from cloudharness.auth import AuthClient


class Command(BaseCommand):
    help = "Sends an update account email to all keycloak users. " \
           "The email contains link the user can click to perform a set of required actions. "

    def __init__(self):
        super().__init__()
        self.keycloak_admin = AuthClient().get_admin_client()

    def handle(self, *args, **options):
        for user in self.keycloak_admin.get_users():
            self._send_email(user)

    @refresh_keycloak_client
    def _send_email(self, user):
        self.keycloak_admin.send_update_account(user['id'], [KeycloakRequiredActions.UPDATE_PASSWORD.value])
