from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TargetSerializer
from .models import Target


def target_map(request):
    return render(request, 'target/map.html')


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    queryset = Target.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            qs = Target.objects.all()
        else:
            qs = Target.objects.filter(user=user)
        return qs
