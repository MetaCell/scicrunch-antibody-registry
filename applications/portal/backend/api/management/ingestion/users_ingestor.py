from typing import Dict

import pandas as pd

from areg_portal.settings import ORCID_URL, USERS_RELEVANT_HEADER
from cloudharness.auth import AuthClient


class UsersIngestor:
    def __init__(self, users_data_path):
        self.users_df = pd.read_csv(users_data_path, dtype='unicode')
        self.users_df = self.users_df.where(pd.notnull(self.users_df), '')
        self.keycloak_admin = AuthClient().get_admin_client()

    def get_users_map(self) -> Dict:
        users = [self._create_keycloak_user_from_row(*row) for row in
                 self.users_df[USERS_RELEVANT_HEADER].to_numpy()]
        # todo: return map guid -> keycloak id afonsobspinto
        return {}

    def _create_keycloak_user_from_row(self, *args):
        row = dict(zip(USERS_RELEVANT_HEADER, args))
        return self.keycloak_admin.create_user({"email": row['email'],
                                                "username": _get_unique_username(row),
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
                                                "requiredActions": ['VERIFY_EMAIL', 'UPDATE_PASSWORD']
                                                }, exist_ok=True)


def _get_unique_username(row) -> str:
    return f"{row['guid']}" if row["firstName"] == '' else f"{row['firstName']}_{row['guid']}"


def _get_orcid_id(row) -> str:
    return '' if row['orcid_id'] == '' else f"{ORCID_URL}{row['orcid_id']}"
