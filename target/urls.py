from django.urls import path, include
from rest_framework import routers
from .views import TargetViewSet

router = routers.SimpleRouter()
router.register('targets', TargetViewSet)

urlpatterns = path('', include(router.urls)),
