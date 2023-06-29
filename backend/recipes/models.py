from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', max_length=255)
    measurement_unit = models.CharField('Единицы измерения', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField('Тег', max_length=255, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.quantity}'
            f' {self.ingredient.measurement_unit}'
        )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='shopping_lists',
        verbose_name='Рецепты'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

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
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'
