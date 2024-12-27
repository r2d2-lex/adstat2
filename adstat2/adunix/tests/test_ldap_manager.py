import logging
import unittest
from unittest.mock import patch, MagicMock
from ldap3.core.exceptions import LDAPKeyError, LDAPCursorAttributeError
from ..ldap_manager import LdapManager, make_attribute_records


class TestLdapManager(unittest.TestCase):

    @patch('ldap3.Server')
    @patch('ldap3.Connection')
    def setUp(self, mock_connection, mock_server):
        self.mock_server = mock_server.return_value
        self.mock_connection = mock_connection.return_value
        self.ldap_manager = LdapManager('hostname', 'username', 'password', 'DC=domain,DC=com')
        self.ldap_manager.connection = self.mock_connection

    def test_update_user_values_success(self):
        self.mock_connection.result = {'result': 0, 'description': 'success'}
        attributes = {'displayName': 'New Name'}
        result, status = self.ldap_manager.update_user_values('CN=TestUser,OU=Users,OU=TEST_GROUP,DC=DOMAIN,DC=COM', attributes)

        self.assertTrue(result)
        self.assertIn('Атрибут displayName успешно изменен на New Name.', status)

    def test_update_user_values_failure(self):
        self.mock_connection.result = {'result': 1, 'description': 'error'}
        attributes = {'displayName': 'New Name'}
        result, status = self.ldap_manager.update_user_values('CN=TestUser,OU=Users,OU=TEST_GROUP,DC=DOMAIN,DC=COM', attributes)

        self.assertFalse(result)
        self.assertIn('Ошибка при изменении атрибута displayName:', status)

    def test_get_users(self):
        self.mock_connection.entries = [MagicMock(), MagicMock()]
        self.mock_connection.entries[0].sAMAccountName = 'user1'
        self.mock_connection.entries[1].sAMAccountName = 'user2'

        users = self.ldap_manager.get_users()
        self.assertEqual(len(users), 2)

    def test_get_groups_list(self):
        self.mock_connection.entries = [MagicMock(), MagicMock()]
        self.mock_connection.entries[0].cn = 'group1'
        self.mock_connection.entries[1].cn = 'group2'

        groups = self.ldap_manager.get_groups_list()
        self.assertEqual(len(groups), 2)

    def test_get_user_list(self):
        self.mock_connection.entries = [MagicMock(), MagicMock()]
        self.mock_connection.entries[0].sAMAccountName = 'user1'
        self.mock_connection.entries[1].sAMAccountName = 'user2'

        users = self.ldap_manager.get_users_list()
        self.assertEqual(len(users), 2)

    def test_make_attribute_records_master_attribute_must_exists(self):
        self.mock_connection.entries = [{'test': 'test'}]
        try:
            make_attribute_records(self.mock_connection, 'Non_Exiten','Not_exiten_attribute', None)
        except KeyError:
            self.fail('Master attribute must exists')


if __name__ == '__main__':
    unittest.main()
