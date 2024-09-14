from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from apps.core.models import User


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users"""

    ordering = ["id"]
    list_display = ["email", "name", "is_staff", "is_active"]
    search_fields = ["email", "name"]

    # Wrap section titles and field names with gettext_lazy for translation
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

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

    readonly_fields = ["last_login", "date_joined"]


# Register the User model with custom UserAdmin
admin.site.register(User, UserAdmin)
