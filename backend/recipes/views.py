from rest_framework import viewsets
from .models import (
    Ingredient,
    Tag,
    Recipe,
    ShoppingList,
    Favorite
)
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    ShoppingListSerializer,
    FavoriteSerializer,
    CreateShoppingListSerializer,
    CreateFavoriteSerializer,
    UserFavoriteSerializer
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateShoppingListSerializer
        return self.serializer_class


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFavoriteSerializer
        elif self.action == 'list':
            return UserFavoriteSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
