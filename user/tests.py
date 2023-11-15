"""Test cases for user app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

test_user = {"username": "testuser@example.com", "password": "testpass"}


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.user = get_user_model().objects.create_user(**test_user)

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_login_view_post(self):
        response = self.client.post(self.login_url, test_user)
        self.assertEqual(response.status_code, 302)  # Should redirect after login


class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("logout")
        self.user = get_user_model().objects.create_user(**test_user)

    def test_logout_view(self):
        self.client.login(**test_user)  # Login first
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
