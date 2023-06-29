from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')
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
