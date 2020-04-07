from django.conf import settings
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Target, Topic


class TargetSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'user', 'title', 'radius', 'location', 'topic']
        read_only_fields = ['user']
        geo_field = 'location'

    def check_max_num_of_targets(self, user):
        num_current_targets = Target.objects.filter(user=user).count()
        if num_current_targets >= settings.MAX_NUMBER_OF_TARGETS:
            msg = f"It is not possible to create more than {settings.MAX_NUMBER_OF_TARGETS} targets."
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        if not request.user.is_superuser:
            self.check_max_num_of_targets(request.user)

        return super(TargetSerializer, self).create(validated_data)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
