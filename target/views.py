import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import TargetSerializer, TopicSerializer
from .models import Target, Topic


@login_required(login_url='rest_login')
def target_map(request):
    data = {
        'google_api_key': os.getenv('GOOGLE_API_KEY')
    }
    return render(request, 'target/map.html', data)


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
        return [IsAuthenticated()] if self.action == 'list' else [IsAdminUser()]
