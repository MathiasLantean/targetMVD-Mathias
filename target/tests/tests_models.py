from django.contrib.gis.geos import Point
from django.test import TestCase

from profile.models import User
from ..models import Target, Topic


class TargetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test@test.com'
        cls.user_password = 'test123455'

    def setUp(self):
        self.test_superuser = User.objects.create_user(
            email='defaultadmin@defaultadmin.com',
            password=self.user_password,
            gender=1,
            is_superuser=True,
        )
        self.test_topic = Topic.objects.create(
            title='topic test',
            photo=None,
        )
        self.test_target = Target.objects.create(
            user=self.test_superuser,
            title='target test',
            radius=45000.02,
            location=Point(-56.164532, -34.901112),
            topic=self.test_topic,
        )

    def test_str_topic(self):
        str_topic = "{} - {}".format(self.test_topic.pk, self.test_topic.title)
        self.assertEqual(str(self.test_topic), str_topic)

    def test_str_target(self):
        str_target = '{} - {}, {}'.format(self.test_target.pk, self.test_target.user.email, self.test_target.title)
        self.assertEqual(str(self.test_target), str_target)
