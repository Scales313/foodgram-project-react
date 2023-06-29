from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import User, Follow
from .permissions import IsAdminRole
from .serializers import UserSerializer, FollowSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def unfollow(self, request, pk=None):
        try:
            follow = Follow.objects.get(pk=pk)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAdminRole]
