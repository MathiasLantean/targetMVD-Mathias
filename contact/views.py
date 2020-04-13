from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail

from contact.models import Information
from contact.serializers import InformationSerializer, QuestionSerializer
from profile.models import User


class InformationDetail(GenericViewSet, RetrieveModelMixin):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class SendQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        admin_users = User.objects.filter(is_superuser=True).values_list('email', flat=True)
        send_mail(
            'You have a new question.',
            data.get('question'),
            request.user.email,
            admin_users,
            fail_silently=False,
        )
        return Response()
