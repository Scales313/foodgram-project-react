from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from users.models import User
from django.conf import settings

MAX_VALUE = settings.MAX_VALUE
MIN_VALUE = settings.MIN_VALUE
IMAGE_THUMBNAIL_SIZE = settings.IMAGE_THUMBNAIL_SIZE


class UserReadSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            return obj.following.filter(user=request.user).exists()
        return False


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')

    def validate(self, obj):
        invalid_usernames = ['me', 'set_password',
                             'subscriptions', 'subscribe']
        if self.initial_data.get('username') in invalid_usernames:
            raise serializers.ValidationError(
                {'username': 'Вы не можете использовать этот username.'}
            )
        return obj


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неверный пароль.'}
            )
        if (
            validated_data['current_password']
            == validated_data['new_password']
        ):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', 'tags')


class FollowsSerializer(serializers.ModelSerializer):
    is_follow = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_follow', 'recipes', 'recipes_count')

    def get_is_follow(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and obj.followers.filter(user=request.user).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def validate(self, data):
        request = self.context.get('request')
        author = self.instance

        if request.user == author:
            raise serializers.ValidationError(
                "Невозможно подписаться на самого себя."
            )

        return data


class FollowAuthorSerializer(FollowsSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError({'errors': 'Ошибка подписки.'})
        return obj


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return obj.shopping_lists.filter(user=request.user).exists()
        return False

    def add_to_shopping_cart(self, user, recipe):
        if not ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            ShoppingList.objects.create(user=user, recipe=recipe)
        else:
            raise serializers.ValidationError(
                {'errors': 'Вы уже добавили этот рецепт.'}
            )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    author = UserReadSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE
    )

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')

    def validate(self, obj):
        required_fields = ['name', 'text', 'cooking_time']
        for field in required_fields:
            if not obj.get(field):
                raise serializers.ValidationError(
                    f'{field} - Обязательное поле.'
                )
        name = obj.get('name')
        if Recipe.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                'Рецепт с таким названием уже существует.',
                code='duplicate_name'
            )

        if not obj.get('tags'):
            raise serializers.ValidationError('Минимум 1 тег.')

        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                'Минимум 1 ингредиент.'
            )

        ingredient_ids = [item['id'] for item in obj.get('ingredients')]
        unique_ingredient_ids = set(ingredient_ids)
        if len(ingredient_ids) != len(unique_ingredient_ids):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )

        return obj

    @transaction.atomic
    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(pk=ingredient['id']),
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.tags_and_ingredients_set(instance, tags, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance,
                                    context=self.context).data
