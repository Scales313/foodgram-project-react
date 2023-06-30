from django.core.validators import RegexValidator
from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag,
)
from users.models import User, Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')


class CustomUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email',
            'first_name', 'last_name', 'role',
            'following', 'followers'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_following(self, obj):
        return FollowSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowSerializer(obj.followers.all(), many=True).data


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


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'title',
            'image',
            'description',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.shopping_lists.filter(user=request.user).exists()
        return False


class ShoppingListSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'recipes']


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'recipe']


class CreateShoppingListSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = ShoppingList
        fields = ['recipes']

    def create(self, validated_data):
        user = self.context['request'].user
        recipes = validated_data['recipes']
        shopping_list = ShoppingList.objects.create(user=user)
        shopping_list.recipes.set(recipes)
        return shopping_list


class CreateFavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['recipe']

    def create(self, validated_data):
        user = self.context['request'].user
        recipe = validated_data['recipe']
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        return favorite


class UserFavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'recipe']
