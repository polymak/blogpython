from django.contrib import admin
from .models import Blog, CustomUser

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'date_joined']
    list_filter = ['role', 'date_joined']
    search_fields = ['username', 'email']
    readonly_fields = ['date_joined']