from django.contrib.auth.models import AbstractUser
from django.core.validators import (EmailValidator, MinLengthValidator,
                                    RegexValidator)
from django.db import models


class UserRole(models.TextChoices):
    GUEST = 'guest', 'Гость'
    USER = 'user', 'Авторизованный пользователь'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
        validators=[EmailValidator(message='Введите корректный адрес email.')]
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9_]+$',
                message=(
                    'Логин может содержать только латинские буквы, ',
                    'цифры и символ подчеркивания.'
                )
            ),
            MinLengthValidator(
                5,
                message='Логин должен содержать не менее 5 символов.'
            )
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        validators=[
            RegexValidator(
                r'^[A-Za-zА-Яа-яЁё\s-]+$',
                message='Имя может содержать только буквы, пробелы и дефисы.'
            ),
            MinLengthValidator(
                2,
                message='Имя должно содержать не менее 2 символов.'
            )
        ]
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        validators=[
            RegexValidator(
                r'^[A-Za-zА-Яа-яЁё\s-]+$',
                message=(
                    'Фамилия может содержать только буквы, пробелы и дефисы.'
                )
            ),
            MinLengthValidator(
                2,
                message='Фамилия должна содержать не менее 2 символов.'
            )
        ]
    )
    role = models.CharField(
        'Уровень доступа',
        max_length=20,
        choices=UserRole.choices
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} оформил подписку на {self.author}'
