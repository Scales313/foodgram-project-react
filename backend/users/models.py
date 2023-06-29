from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('guest', 'Гость'),
        ('user', 'Авторизованный пользователь'),
        ('admin', 'Администратор')
    ]

    username = models.CharField('Логин', max_length=150, unique=True)
    password = models.CharField('Пароль', max_length=128)
    email = models.EmailField('Email', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    role = models.CharField('Уровень доступа', max_length=20, choices=ROLES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
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
