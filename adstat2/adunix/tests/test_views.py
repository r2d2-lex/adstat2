from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch, MagicMock


class TestRegister(TestCase):

    def test_user_reqired_auth(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/admin/login/?next=/')


class TestIndex(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@domain.com', password='testpass', is_staff=True)
        self.client.force_login(self.user)

    @patch('adunix.views.LdapManager')
    def test_index_view(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.get_groups_list.return_value = [
            {'cn': 'group1', 'gidNumber': 1001, 'description': 'Group 1'},
            {'cn': 'group2', 'gidNumber': 1002, 'description': 'Group 2'},
        ]
        mock_ldap_manager.get_users_list.return_value = [
            {'sAMAccountName': 'user1', 'uidNumber': 1001, 'cn': 'User One'},
            {'sAMAccountName': 'user2', 'uidNumber': 1002, 'cn': 'User Two'},
        ]

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adunix/index.html')

        self.assertIn('groups', response.context)
        self.assertIn('users', response.context)
        self.assertIn('max_uid', response.context)

        self.assertEqual(len(response.context['groups']), 2)
        self.assertEqual(len(response.context['users']), 2)
        self.assertEqual(response.context['max_uid'], 1002)
