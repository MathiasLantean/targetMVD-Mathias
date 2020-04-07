import factory
from faker.providers import BaseProvider
from django.contrib.gis.geos import Point
from profile.tests.factories import AdminUserFactory
from target.models import Topic, Target


class DjangoGeoPointProvider(BaseProvider):

    def geo_point(self, **kwargs):
        kwargs.pop('coords_only', None)
        faker = factory.Faker('local_latlng', coords_only=True, **kwargs)
        coords = faker.generate()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    title = factory.Sequence(lambda n: 'TopicTest%d' % n)
    photo = factory.django.ImageField(color='blue')


class TargetFactory(factory.django.DjangoModelFactory):
    factory.Faker.add_provider(DjangoGeoPointProvider)

    class Meta:
        model = Target

    user = factory.SubFactory(AdminUserFactory)
    title = factory.Sequence(lambda n: 'TargetTest%d' % n)
    radius = factory.Faker('random_int', min=4500, max=90000)
    location = factory.Faker('geo_point', country_code='US')
    topic = factory.SubFactory(TopicFactory)
