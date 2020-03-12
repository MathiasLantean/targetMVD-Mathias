"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from profile.views import FacebookLogin, facebook_token

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^rest/', include('rest_framework.urls')),
    url(r'^auth/', include('dj_rest_auth.urls')),
    url(r'^auth/registration/', include(('dj_rest_auth.registration.urls', 'auth'))),
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^auth/facebooktoken/$', facebook_token, name='fb_token'),
    url('^', include('allauth.account.urls')),
    url('^api/', include(('profile.urls', 'app-profile'))),
]
