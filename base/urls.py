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
from django.contrib import admin
from django.urls import path, re_path, include
from profile.views import facebook_token, password_reset
from target.views import target_map
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('target.urls')),
    path('api/v1/', include('profile.urls')),
    path('facebook-token/', facebook_token, name='fb_token'),
    path('map/', target_map, name='target_map'),
    re_path(
        r"^password/reset/key/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        password_reset,
        name="account_reset_password_from_key"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
