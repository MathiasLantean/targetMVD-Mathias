from django.urls import path

from contact.views import InformationDetail

urlpatterns = [
    path('information/<slug:pk>/', InformationDetail.as_view(), name='info'),
]
