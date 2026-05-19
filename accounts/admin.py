from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['gamertag', 'user', 'role', 'province', 'created_at']
    list_filter = ['role', 'province']
    search_fields = ['gamertag', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']