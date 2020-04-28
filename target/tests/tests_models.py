from django.contrib.gis.geos import Point
from django.test import TestCase
from geopy.distance import distance as geopy_distance

from profile.tests.factories import AdminUserFactory
from target.tests.factories import TargetFactory, TopicFactory


def targets_intersect(target_a, target_b):
    distance_between_centers = geopy_distance(
        (target_a.location.y, target_a.location.x),
        (target_b.location.y, target_b.location.x)
    ).meters

    return float(target_a.radius + target_b.radius) >= distance_between_centers


class TargetTests(TestCase):

    def setUp(self):
        self.test_superuser = AdminUserFactory()
        self.test_topic = TopicFactory()
        self.test_target = TargetFactory(
            user=self.test_superuser,
            topic=self.test_topic,
        )
        self.point_a = Point((-118.25508, 34.14251))
        self.point_b = Point((-119.25499999999995, 35.14260999999997))

    def test_str_target(self):
        str_target = '{} - {}, {}'.format(self.test_target.pk, self.test_target.user.email, self.test_target.title)
        self.assertEqual(str(self.test_target), str_target)

    def test_get_matches_ok(self):
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000, topic=target_a.topic)
        matches = list(target_a.get_matches())
        self.assertTrue(targets_intersect(target_a, target_b))
        self.assertEqual(len(matches), 1)

    def test_get_matches_no_match_because_no_intersection(self):
        target_a = TargetFactory(location=self.point_a, radius=500)
        target_b = TargetFactory(location=self.point_b, radius=500, topic=target_a.topic)
        matches = list(target_a.get_matches())
        self.assertFalse(targets_intersect(target_a, target_b))
        self.assertEqual(len(matches), 0)

    def test_get_matches_no_match_because_different_topic(self):
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000)
        matches = list(target_a.get_matches())
        self.assertTrue(targets_intersect(target_a, target_b))
        self.assertEqual(len(matches), 0)

    def test_get_matches_no_match_because_same_user(self):
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000, topic=target_a.topic, user=target_a.user)
        matches = list(target_a.get_matches())
        self.assertTrue(targets_intersect(target_a, target_b))
        self.assertEqual(len(matches), 0)


class TopicTests(TestCase):
    def setUp(self):
        self.test_topic = TopicFactory()

    def test_str_topic(self):
        str_topic = "{} - {}".format(self.test_topic.pk, self.test_topic.title)
        self.assertEqual(str(self.test_topic), str_topic)
