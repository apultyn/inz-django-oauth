from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import Group


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, keycloak_id=None, **other):
        other.setdefault("is_active", True)
        if not email:
            raise ValueError("You must provide an email")

        email = self.normalize_email(email)
        user = self.model(email=email, keycloak_id=keycloak_id, **other)
        user.set_unusable_password()

        user.save()
        return user

    def create_superuser(self, email, **other):
        other.setdefault("is_staff", True)
        other.setdefault("is_superuser", True)
        other.setdefault("is_active", True)

        if other.get("is_staff") is not True:
            raise ValueError("Superuser must be staff")

        if other.get("is_superuser") is not True:
            raise ValueError("Superuser must be is_superuser=True")

        return self.create_user(email, keycloak_id=None, **other)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    keycloak_id = models.CharField(max_length=50, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
