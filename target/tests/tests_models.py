from django.test import TestCase

from profile.tests.factories import AdminUserFactory
from target.tests.factories import TargetFactory, TopicFactory


class TargetTests(TestCase):

    def setUp(self):
        self.test_superuser = AdminUserFactory()
        self.test_topic = TopicFactory()
        self.test_target = TargetFactory(
            user=self.test_superuser,
            topic=self.test_topic,
        )

    def test_str_topic(self):
        str_topic = "{} - {}".format(self.test_topic.pk, self.test_topic.title)
        self.assertEqual(str(self.test_topic), str_topic)

    def test_str_target(self):
        str_target = '{} - {}, {}'.format(self.test_target.pk, self.test_target.user.email, self.test_target.title)
        self.assertEqual(str(self.test_target), str_target)
