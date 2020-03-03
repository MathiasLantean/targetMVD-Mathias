from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from account.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
