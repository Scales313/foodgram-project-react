from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active'
    )
    list_filter = ('is_active', 'first_name', 'email')
    search_fields = ('username', 'email')
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'role'
            ),
        }),
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
