from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Recipe, Ingredient, Tag


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active'
    ]
    list_filter = ['is_active', 'email', 'username']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['author', 'title', 'tags']
    search_fields = ['title', 'author__username']
    ordering = ['title']
    readonly_fields = ['favorite_count']

    def favorite_count(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']
    ordering = ['name']
