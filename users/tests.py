from django.urls import path, include

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from .models import NewUser


class AuthITTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/auth/", include("users.urls"))]

    def setUp(self):
        self.user = NewUser.objects.create_user(
            password="passwd", email="user@example.com"
        )

    def test_login_success(self):
        response = self.client.post(
            "/api/auth/login/",
            format="json",
            data={"email": "user@example.com", "password": "passwd"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data.keys())

    def test_login_wrong_passwd(self):
        response = self.client.post(
            "/api/auth/login/",
            format="json",
            data={"email": "user@example.com", "password": "passwddasf"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_email(self):
        response = self.client.post(
            "/api/auth/login/",
            format="json",
            data={"email": "userple.com", "password": "passwddasf"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_success(self):
        response = self.client.post(
            "/api/auth/register/",
            format="json",
            data={
                "email": "apultyn@example.com",
                "password": "passwd",
                "confirm_password": "passwd",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"email": "apultyn@example.com"})

    def test_register_passwd_missmatch(self):
        response = self.client.post(
            "/api/auth/register/",
            format="json",
            data={
                "email": "apultyn@example.com",
                "password": "passsfdgwd",
                "confirm_password": "passwd",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
