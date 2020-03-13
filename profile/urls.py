from django.conf.urls import url
from django.urls import include
from profile.views import FacebookLogin

urlpatterns = [
    url(r'^registration/', include(('dj_rest_auth.registration.urls', 'auth'))),
    url(r'^facebook/$', FacebookLogin.as_view(), name='fb_login'),
]
