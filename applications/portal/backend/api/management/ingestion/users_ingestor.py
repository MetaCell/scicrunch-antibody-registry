import logging
from enum import Enum
from typing import Dict
from api.services.keycloak_service import KeycloakService

import pandas as pd

from api.utilities.decorators import timed_class_method
from portal.settings import ORCID_URL, USERS_RELEVANT_HEADER, GUID_INDEX, PROVIDER_ID, EMAIL_INDEX
from pydantic import validate_email


class KeycloakRequiredActions(Enum):
    UPDATE_PASSWORD = 'UPDATE_PASSWORD'
    VERIFY_EMAIL = 'VERIFY_EMAIL'


class UsersIngestor:
    def __init__(self, users_data_path, keycloak_service: KeycloakService):
        self.users_df = pd.read_csv(users_data_path, dtype='unicode')
        self.users_df = self.users_df.where(pd.notnull(self.users_df), '')
        self.keycloak_service: KeycloakService = keycloak_service

    @timed_class_method('Keycloak users added')
    def ingest_users(self) -> Dict:
        users = {}
        for row in self.users_df[USERS_RELEVANT_HEADER].to_numpy():
            try:
                users[str(int(float(row[GUID_INDEX])))
                      ] = self._get_or_create_keycloak_user_from_row(*row)
            except Exception as e:
                logging.error(
                    f"Cannot add user {row[EMAIL_INDEX]} -- GUID {row[GUID_INDEX]}: {e}")
        return users

    def _get_or_create_keycloak_user_from_row(self, *args):

        row = dict(zip(USERS_RELEVANT_HEADER, args))
        if not row['guid']:
            raise Exception("GUID is empty")

        if not row['email']:
            raise Exception("Email is empty")
        validate_email(row['email'])

        existent_user = self.keycloak_service.get_user_by_username(
            row['email'])
        if existent_user:
            return existent_user['id']
        logging.info(f"Creating user {row['email']}")
        user_id = self.keycloak_service.create_user(
            {"email": row['email'],
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
        if row['orcid_id'] != '':
            try:
                self.keycloak_service.add_user_social_login(
                    user_id, PROVIDER_ID, row['orcid_id'], row['orcid_id'])
            except:
                logging.error(f"Cannot add social login for user {user_id}")
        return user_id


def _get_orcid_id(row) -> str:
    return '' if row['orcid_id'] == '' else f"{ORCID_URL}{row['orcid_id']}"
