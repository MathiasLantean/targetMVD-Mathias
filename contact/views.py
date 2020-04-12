from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from contact.models import Information
from contact.serializers import InformationSerializer


class InformationDetail(APIView):
    def get_object(self, pk):
        try:
            return Information.objects.get(pk=pk)
        except Information.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        info = self.get_object(pk)
        serializer = InformationSerializer(info)
        return Response(serializer.data)
