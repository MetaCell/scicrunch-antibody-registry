from typing import Dict

import pandas as pd

from api.utilities.decorators import refresh_keycloak_client, timed_class_method
from areg_portal.settings import ORCID_URL, USERS_RELEVANT_HEADER, GUID_INDEX
from cloudharness.auth import AuthClient

from enum import Enum


class KeycloakRequiredActions(Enum):
    UPDATE_PASSWORD = 'UPDATE_PASSWORD'
    VERIFY_EMAIL = 'VERIFY_EMAIL'


class UsersIngestor:
    def __init__(self, users_data_path):
        self.users_df = pd.read_csv(users_data_path, dtype='unicode')
        self.users_df = self.users_df.where(pd.notnull(self.users_df), '')
        self.keycloak_admin = AuthClient().get_admin_client()

    @timed_class_method('Keycloak users added')
    def get_users_map(self) -> Dict:
        return {str(int(float(row[GUID_INDEX]))): self._create_keycloak_user_from_row(*row) for row in
                self.users_df[USERS_RELEVANT_HEADER].to_numpy() if row[GUID_INDEX] != ''}

    @refresh_keycloak_client
    def _create_keycloak_user_from_row(self, *args):
        row = dict(zip(USERS_RELEVANT_HEADER, args))
        return self.keycloak_admin.create_user({"email": row['email'],
                                                "username": row['email'],
                                                "enabled": True,
                                                "firstName": row['firstName'],
                                                "lastName": row['lastName'],
                                                "attributes": {
                                                    "orcid": _get_orcid_id(row),
                                                    "id": row['id'],
                                                    "guid": row['guid'],
                                                    "level": row['level'],
                                                    "middleInitial": row['middleInitial'],
                                                    "organization": row['organization'],
                                                    "created": row['created'],
                                                },
                                                "requiredActions": [KeycloakRequiredActions.UPDATE_PASSWORD.value]
                                                }, exist_ok=True)


def _get_orcid_id(row) -> str:
    return '' if row['orcid_id'] == '' else f"{ORCID_URL}{row['orcid_id']}"
