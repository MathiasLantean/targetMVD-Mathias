from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'gender', 'is_superuser', 'password',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

