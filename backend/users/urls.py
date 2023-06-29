from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'follows', FollowViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
]
