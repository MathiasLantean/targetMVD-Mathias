import factory
from contact.models import Information


class InformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Information

    title = factory.Faker('word')
    detail = factory.Faker('paragraph', nb_sentences=15)
