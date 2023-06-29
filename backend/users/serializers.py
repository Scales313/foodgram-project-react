from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'password', 'email',
            'first_name', 'last_name', 'role'
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')


class GetCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex='^((?!me).)[a-zA-Z0-9+_@.-]*$',
                message='Использованы недопустимые символы',
                code='invalid_username'
            ),
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=150,
    )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9+_@.-]*$',
                message='Использованы недопустимые символы',
                code='invalid_username'
            ),
        ],
    )
    confirmation_code = serializers.CharField(required=True)
