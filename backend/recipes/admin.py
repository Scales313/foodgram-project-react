from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Tag)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2
    min_num = 1


@admin.register(RecipeIngredient)
class LinksAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    recipes = ('user', 'recipe__name', 'date_added')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe_name')
    search_fields = ('user__username', 'recipe__name')

    def recipe_name(self, obj):
        return obj.recipe.name

    recipe_name.short_description = 'Recipe Name'


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
    list_display = ['name', 'author']
    list_filter = ['author', 'tags']
    search_fields = ['name', 'author__username']
    ordering = ['name']
    readonly_fields = ['favorite_count']
    inlines = [IngredientInline]

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
