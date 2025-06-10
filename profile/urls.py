from django.urls import path, include
from profile.views import FacebookLogin, AdminListUsers

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('allauth.account.urls')),
    path('users/', AdminListUsers.as_view(), name='user_list'),
    path('registration/', include(('dj_rest_auth.registration.urls', 'auth'))),
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
]
