from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone
from PIL import Image

from foodgram.settings import MAX_VALUE, MIN_VALUE, IMAGE_THUMBNAIL_SIZE


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', max_length=255)
    measurement_unit = models.CharField('Единицы измерения', max_length=255)

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField('Тег', max_length=255, unique=True)
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Цвет должен быть в формате HEX.',
            ),
        ],
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=255
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор рецепта',
        null=True
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/',
    )
    text = models.TextField(verbose_name='Описание блюда',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(MIN_VALUE, 'Не меньше одного'),
            MaxValueValidator(MIN_VALUE, 'Слишком большое время')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        default=timezone.now
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail(IMAGE_THUMBNAIL_SIZE)
            img.save(self.image.path)


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В каких рецептах',
        related_name='recipe_ingredient',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Связанные ингредиенты',
        related_name='recipe_ingredient',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=[
            MinValueValidator(MIN_VALUE, 'Не меньше одного'),
            MaxValueValidator(MAX_VALUE, 'Просто съешь это отдельно')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'Список покупок #{self.pk} - {self.user.username}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Понравившиеся'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
