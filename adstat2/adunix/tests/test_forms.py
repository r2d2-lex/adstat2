from django import forms
from django.test import TestCase
from ..forms import UnixAttrsForm


class UnixAttrsFormTest(TestCase):

    def test_form_valid_data(self):
        form_data = {
            'distinguishedName': 'cn=example,dc=com',
            'gidNumber': 1000,
            'uid': 'exampleuser',
            'msSFU30Name': 'exampleName',
            'msSFU30NisDomain': 'exampleDomain',
            'uidNumber': 1001,
            'loginShell': '/bin/bash',
            'unixHomeDirectory': '/home/exampleuser',
        }
        form = UnixAttrsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'distinguishedName': '',
            'gidNumber': 'not_a_number',
            'uid': 'exampleuser',
            'msSFU30Name': 'exampleName',
            'msSFU30NisDomain': 'exampleDomain',
            'uidNumber': 1001,
            'loginShell': '/bin/bash',
            'unixHomeDirectory': '/home/exampleuser',
        }
        form = UnixAttrsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('distinguishedName', form.errors)
        self.assertIn('gidNumber', form.errors)
