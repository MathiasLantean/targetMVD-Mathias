import factory
from factory import SubFactory

from target.tests.factories import TargetFactory
from contact.models import Information, Chat


class InformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Information

    title = factory.Faker('word')
    detail = factory.Faker('paragraph', nb_sentences=15)


class ChatFactory(factory.django.DjangoModelFactory):
    target_one = SubFactory(TargetFactory)
    target_two = SubFactory(TargetFactory)

    class Meta:
        model = Chat
