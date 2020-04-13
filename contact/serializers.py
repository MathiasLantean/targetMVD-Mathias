from rest_framework import serializers
from contact.models import Information


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(allow_blank=False, allow_null=False)
