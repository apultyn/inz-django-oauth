from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import Textarea

from .models import NewUser


@admin.register(NewUser)
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ("email",)
    ordering = ["id"]
    list_filter = ("email", "is_active", "is_staff")
    list_display = (
        "email",
        "id",
        "is_active",
        "is_staff",
        "password",
    )
    fieldsets = (
        (
            None,
            {"fields": ("email",)},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
