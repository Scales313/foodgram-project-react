from django.urls import include, path
from rest_framework import routers
from .views import (
    IngredientViewSet,
    TagViewSet,
    RecipeViewSet,
    ShoppingListViewSet,
    FavoriteViewSet
)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'shopping-lists', ShoppingListViewSet)
router.register(r'favorites', FavoriteViewSet)

app_name = 'your_app_name'

urlpatterns = [
    path('', include(router.urls)),
]
