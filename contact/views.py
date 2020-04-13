from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from contact.models import Information
from contact.serializers import InformationSerializer


class InformationDetail(GenericViewSet, RetrieveModelMixin):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
