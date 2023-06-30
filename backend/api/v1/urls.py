from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    FollowViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    ShoppingListViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('follows', FollowViewSet)
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register(
    'shopping-lists',
    ShoppingListViewSet,
    basename='shopping-list'
)

urlpatterns = [
    path('', include(router.urls)),
]
