from django.contrib.auth.models import User
from django.test import TestCase


class TestIndex(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@domain.com', password='testpass', is_staff=True)
        self.client.force_login(self.user)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adunix/index.html')
