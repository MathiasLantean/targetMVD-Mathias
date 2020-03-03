from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .Serializers import UserSerializer
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

