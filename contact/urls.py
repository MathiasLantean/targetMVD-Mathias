from django.urls import path, include
from rest_framework import routers

from contact.views import InformationDetail, SendQuestion

router = routers.SimpleRouter()
router.register(r'information', InformationDetail, basename='info')

urlpatterns = [
    path('questions/', SendQuestion.as_view(), name='send_question'),
    path('', include(router.urls)),
]
