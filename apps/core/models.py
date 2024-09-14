"""
Database Models
"""

from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager for User model that uses email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a regular user with an email and password.
        Regular users cannot be staff or superusers.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))

        if not password:
            raise ValueError(_("A password must be set for regular users."))

        email = self.normalize_email(email)

        # Only enforce is_staff and is_superuser to be False if they are not already set
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Limit the fields to prevent arbitrary field injection
        allowed_fields = {
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        }
        filtered_extra_fields = {
            k: v for k, v in extra_fields.items() if k in allowed_fields
        }

        user = self.model(email=email, **filtered_extra_fields)
        # Salt and Hashed password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser with is_staff=True and is_superuser=True.
        Enforce these fields to True and prevent arbitrary values.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not password:
            raise ValueError(_("Superusers must have a password."))

        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        # Allow the same limited fields but force is_staff and is_superuser to True
        allowed_fields = {
            "name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        }
        filtered_extra_fields = {
            k: v for k, v in extra_fields.items() if k in allowed_fields
        }

        return self.create_user(email, password, **filtered_extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email instead of username"""

    email = models.EmailField(_("email address"), unique=True, max_length=255)
    name = models.CharField(_("username"), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Assign a manager to User ie. UserManager
    objects = UserManager()

    # This tells Django that the "email" field should be used as the unique identifier instead of "username".
    USERNAME_FIELD = "email"

    # Fields required when creating a superuser. We leave this empty since email is required by default
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
