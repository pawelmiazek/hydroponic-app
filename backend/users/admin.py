from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ("email",)
    ordering = ("email",)
    list_display = ("id", "email", "is_superuser", "created_at", "last_login")
