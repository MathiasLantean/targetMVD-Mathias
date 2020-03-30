from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Target, Topic


class TargetSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'user', 'title', 'radius', 'location', 'topic']
        read_only_fields = ['user']
        geo_field = 'location'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super(TargetSerializer, self).create(validated_data)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
