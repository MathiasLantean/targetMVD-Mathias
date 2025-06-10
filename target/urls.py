from django.urls import path, include
from rest_framework import routers
from .views import TargetViewSet, TopicViewSet

router = routers.SimpleRouter()
router.register('targets', TargetViewSet, basename='target')
router.register('topics', TopicViewSet, basename='topic')

urlpatterns = path('', include(router.urls)),
