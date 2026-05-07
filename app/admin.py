from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Hen, EggLog, Breed, Color


@admin.register(Hen)
class HenAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'color', 'date_added', 'is_active']
    list_filter = ['is_active', 'breed', 'color']
    search_fields = ['name', 'breed__name', 'color__name']


@admin.register(EggLog)
class EggLogAdmin(admin.ModelAdmin):
    list_display = ['hen', 'date', 'quantity', 'created_at']
    list_filter = ['date', 'hen']
    search_fields = ['hen__name']
    date_hierarchy = 'date'


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
