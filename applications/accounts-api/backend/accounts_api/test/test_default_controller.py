# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from accounts_api.models.users_userid_password_put_request import UsersUseridPasswordPutRequest  # noqa: E501
from accounts_api.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_users_userid_password_put(self):
        """Test case for users_userid_password_put

        
        """
        users_userid_password_put_request = accounts_api.UsersUseridPasswordPutRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/users/{userid}/password'.format(userid='userid_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(users_userid_password_put_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
