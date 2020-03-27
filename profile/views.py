from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class AdminListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


def facebook_token(request):
    return render(request, 'account/facebook_sign_up.html')


def password_reset(request, uidb64=None, token=None):
    context = {
        'uidb64': uidb64,
        'token': token,
    }
    return render(request, 'registration/password_reset.html', context)
