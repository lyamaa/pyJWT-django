from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

USERNAME_REGEX = "^[a-zA-Z0-9.+-]*$"

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email Address")
    username = models.CharField(max_length=255, validators=[
        RegexValidator(regex=USERNAME_REGEX,
        message='Username must be alphanumeric or contains numbers',
        code='Invalid Username'
        )
    ],
    unique=True
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

