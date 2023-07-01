from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', max_length=255)
    measurement_unit = models.CharField('Единицы измерения', max_length=255)

    def __str__(self):
        return f"{self.name} {self.measurement_unit}"

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
    title = models.CharField(
        verbose_name="Название рецепта",
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
        verbose_name="Изображение блюда",
        upload_to="recipe_images/",
    )
    description = models.TextField(
        verbose_name="Описание блюда",
        max_length=10000)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((300, 300))
            img.save(self.image.path)


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="В каких рецептах",
        related_name="ingredient",
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name="Связанные ингредиенты",
        related_name="recipe",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        default=0,
        validators=[
            MinValueValidator(0, "Может тогда уберешь это из рецепта?)"),
            MaxValueValidator(100, "Просто съешь это отдельно")
        ]
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"


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
        verbose_name='Понравившиеся'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'
