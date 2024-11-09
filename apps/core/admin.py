from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from apps.core.models import User
from . import models


class UserAdmin(BaseUserAdmin):
    """
    Define the admin interface for the User model.

    This class customizes how the User model is presented and managed
    in the Django admin site. It specifies the ordering, display fields,
    search fields, and how user-related fields are grouped and displayed.
    """

    ordering = ["id"]
    """
    Set the default ordering of users by their ID.
    """

    list_display = ["email", "name", "is_staff", "is_active"]
    """
    Define which fields are displayed in the list view of the admin
    interface for users.
    """

    search_fields = ["email", "name"]
    """
    Specify the fields that should be searchable in the admin interface.
    """

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    """
    Define the layout of the user detail form in the admin interface.

    - The first section shows the email and password fields.
    - The second section groups personal information like name.
    - The third section handles permissions such as active status and roles.
    - The fourth section displays important dates like last login and date joined.
    """

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    """
    Define the layout for the user creation form in the admin interface.

    - The `classes` attribute sets styling options for the form.
    - The `fields` attribute specifies which fields should be included in the form.
    """

    readonly_fields = ["last_login", "date_joined"]
    """
    Specify fields that are read-only and cannot be edited in the admin interface.
    """


# Register the User model with the custom UserAdmin configuration
admin.site.register(User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
