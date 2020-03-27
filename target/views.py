from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import TargetSerializer, TopicSerializer
from .models import Target, Topic


def target_map(request):
    return render(request, 'target/map.html')


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    queryset = Target.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            qs = Target.objects.all()
        else:
            qs = Target.objects.filter(user=user)
        return qs


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
