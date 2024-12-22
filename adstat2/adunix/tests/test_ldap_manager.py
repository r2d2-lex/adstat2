import unittest
from unittest.mock import patch, MagicMock

from ..ldap_manager import LdapManager


class TestLdapManager(unittest.TestCase):

    @patch('ldap3.Server')
    @patch('ldap3.Connection')
    def setUp(self, mock_connection, mock_server):
        self.mock_server = mock_server.return_value
        self.mock_connection = mock_connection.return_value
        self.ldap_manager = LdapManager('hostname', 'username', 'password', 'base_dn')
        self.ldap_manager.connection = self.mock_connection

    def test_update_user_values_success(self):
        self.mock_connection.result = {'result': 0, 'description': 'success'}
        attributes = {'displayName': 'New Name'}
        result, status = self.ldap_manager.update_user_values('user_dn', attributes)

        self.assertTrue(result)
        self.assertIn('Атрибут displayName успешно изменен на New Name.', status)

    def test_update_user_values_failure(self):
        self.mock_connection.result = {'result': 1, 'description': 'error'}
        attributes = {'displayName': 'New Name'}
        result, status = self.ldap_manager.update_user_values('user_dn', attributes)

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


if __name__ == '__main__':
    unittest.main()
