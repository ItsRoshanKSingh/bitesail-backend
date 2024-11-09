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
from django.conf import settings


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    This manager handles the creation of regular users and superusers.
    It uses email as the unique identifier instead of the default username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        Regular users are created with default values for `is_staff` and `is_superuser`,
        which are set to False. Raises ValueError if email or password is not provided.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))

        if not password:
            raise ValueError(_("A password must be set for regular users."))

        email = self.normalize_email(email)

        # Default `is_staff` and `is_superuser` to False
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Filter extra fields to include only allowed ones
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

        # Create the user instance with the filtered extra fields
        user = self.model(email=email, **filtered_extra_fields)
        # Set and hash the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with `is_staff=True` and `is_superuser=True`.

        Enforces these fields to True and filters extra fields to include only allowed ones.
        Raises ValueError if email or password is not provided.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not password:
            raise ValueError(_("Superusers must have a password."))

        # Set `is_staff` and `is_superuser` to True for superusers
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        # Filter extra fields to include only allowed ones
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
    """
    Custom User model that uses email as the unique identifier instead of username.

    Includes fields for email, name, and various flags such as `is_staff` and `is_active`.
    The model uses `UserManager` for user management.
    """

    email = models.EmailField(_("email address"), unique=True, max_length=255)
    name = models.CharField(_("username"), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Assign a custom manager to handle user creation and management
    objects = UserManager()

    # Use email as the unique identifier instead of username
    USERNAME_FIELD = "email"

    # Fields required when creating a superuser. Empty since email is required by default.
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Return a string representation of the user instance, which is the user's email.
        """
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe objects"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minute = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
