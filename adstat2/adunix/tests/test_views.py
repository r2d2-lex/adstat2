from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', email='testuser@domain.com', password='testpass', is_staff=True
        )

    def setUp(self):
        self.client.force_login(self.user)


class TestRegister(TestCase):

    def test_user_reqired_auth(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/admin/login/?next=/')
        response = self.client.post('/')
        self.assertRedirects(response, '/admin/login/?next=/')


class TestIndex(UserTestCase):

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

        response = self.client.get(reverse('adunix:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adunix/index.html')

        self.assertIn('groups', response.context)
        self.assertIn('users', response.context)
        self.assertIn('max_uid', response.context)

        self.assertEqual(len(response.context['groups']), 2)
        self.assertEqual(len(response.context['users']), 2)
        self.assertEqual(response.context['max_uid'], 1002)


class GetNewUidViewTests(UserTestCase):

    @patch('adunix.views.LdapManager')
    def test_get_new_uid(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.get_users_list.return_value = [
            {'uidNumber': 1001},
            {'uidNumber': 1002},
            {'uidNumber': 1003},
        ]

        response = self.client.post(reverse('adunix:get_new_uid'))

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertEqual(json_response['uidNumber'], 1004)
        self.assertEqual(json_response['domain'], settings.DOMAIN)

        mock_ldap_manager.get_users_list.assert_called_once_with(['uidNumber'])


class UpdateUserDataViewTests(UserTestCase):

    @patch('adunix.views.LdapManager')
    def test_update_user_data_success(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.update_user_values.return_value = (True, 'Данные успешно обновлены')

        response = self.client.post(reverse('adunix:update_user_data'), {
            'distinguishedName': 'cn=testuser,dc=domain,dc=com',
            'gidNumber': 1001,
            'uid': 'testuser',
            'msSFU30Name': 'testuser',
            'msSFU30NisDomain': 'domain.com',
            'uidNumber': 1001,
            'loginShell': '/bin/bash',
            'unixHomeDirectory': '/home/testuser',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Данные успешно обновлены'})

    @patch('adunix.views.make_errors_result')
    @patch('adunix.views.LdapManager')
    def test_update_user_data_invalid_form(self, MockLdapManager, mock_make_errors_result):
        mock_make_errors_result.return_value = 'Ошибка обновления данных'
        response = self.client.post(reverse('adunix:update_user_data'), {
            'distinguishedName': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Ошибка обновления данных'})


class DeleteUserDataViewTests(UserTestCase):
    @patch('adunix.views.LdapManager')
    def test_delete_user_data_success(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.update_user_values.return_value = (True, 'Данные успешно удалены')

        response = self.client.post(reverse('adunix:delete_user_data'), {
            'distinguishedName': 'cn=testuser,dc=domain,dc=com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Данные успешно удалены'})

    @patch('adunix.views.LdapManager')
    def test_delete_user_data_no_distinguished_name(self, MockLdapManager):
        response = self.client.post(reverse('adunix:delete_user_data'), {
            'distinguishedName': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Ошибка удаления данных'})


class GetUserDataViewTests(UserTestCase):
    @patch('adunix.views.LdapManager')
    def test_get_user_data_success(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.get_sam_user.return_value = [{
            'cn': 'testuser',
            'uid': 'testuser',
            'msSFU30Name': 'testuser',
            'msSFU30NisDomain': 'domain.com',
            'uidNumber': 1001,
            'gidNumber': 1001,
            'loginShell': '/bin/bash',
            'unixHomeDirectory': '/home/testuser',
            'distinguishedName': 'cn=testuser,dc=domain,dc=com',
        }]

        response = self.client.get(reverse('adunix:get_user_data'), {'username': 'testuser'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'cn': 'testuser',
            'uid': 'testuser',
            'msSFU30Name': 'testuser',
            'msSFU30NisDomain': 'domain.com',
            'uidNumber': 1001,
            'gidNumber': 1001,
            'loginShell': '/bin/bash',
            'unixHomeDirectory': '/home/testuser',
            'distinguishedName': 'cn=testuser,dc=domain,dc=com',
            'result_message': 'Данные получены',
            'result': True,
        })

    @patch('adunix.views.LdapManager')
    def test_get_user_data_user_not_found(self, MockLdapManager):
        mock_ldap_manager = MockLdapManager.return_value.__enter__.return_value
        mock_ldap_manager.get_sam_user.side_effect = IndexError

        response = self.client.get(reverse('adunix:get_user_data'), {'username': 'nonexistentuser'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result_message': 'Ошибка загрузки данных', 'result': False})
