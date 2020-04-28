from django.contrib.gis.geos import Point
from django.test import TestCase

from contact.tests.factories import ChatFactory
from target.tests.factories import TargetFactory
from target.target_utils import manage_target_chats


class ChatManagerTests(TestCase):

    def setUp(self):
        self.point_a = Point((-118.25508, 34.14251))
        self.point_b = Point((-119.25499999999995, 35.14260999999997))
        self.point_c = Point((-118.25508, 33.691738292121755))

    def test_manage_target_chats_new_chats(self):
        # Target A matches with B and C. Chats A_B and A_C should be created.
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000, topic=target_a.topic)
        target_c = TargetFactory(location=self.point_c, radius=30000, topic=target_a.topic)
        ChatFactory(target_one=target_b, target_two=target_c)

        manage_target_chats(target_a)

        matches = len(list(target_a.get_matches()))
        chats_target_a = target_a.chat_one_set.count() + target_a.chat_two_set.count()
        self.assertEqual(chats_target_a, matches)

    def test_manage_target_chats_no_new_chats(self):
        # Target A doesn't matches with B nor C. No chats should be created.
        target_a = TargetFactory(location=self.point_a, radius=666)
        target_b = TargetFactory(location=self.point_b, radius=6969, topic=target_a.topic)
        target_c = TargetFactory(location=self.point_c, radius=3030, topic=target_a.topic)
        ChatFactory(target_one=target_b, target_two=target_c)

        manage_target_chats(target_a)

        matches = len(list(target_a.get_matches()))
        chats_target_a = target_a.chat_one_set.count() + target_a.chat_two_set.count()
        self.assertEqual(chats_target_a, matches)

    def test_manage_target_chats_edit_target_radius(self):
        # Target A has A_B and A_C chats. After changing A radius, A doesn't match anymore.
        target_a = TargetFactory(location=self.point_a, radius=666)
        target_b = TargetFactory(location=self.point_b, radius=6969, topic=target_a.topic)
        target_c = TargetFactory(location=self.point_c, radius=3030, topic=target_a.topic)
        ChatFactory(target_one=target_a, target_two=target_b)
        ChatFactory(target_one=target_a, target_two=target_c)

        manage_target_chats(target_a)

        matches = len(list(target_a.get_matches()))
        chats_target_a = target_a.chat_one_set.count() + target_a.chat_two_set.count()
        self.assertEqual(matches, 0)
        self.assertEqual(chats_target_a, matches)

    def test_manage_target_chats_edit_target_user(self):
        # Target A has A_B and A_C chats. After changing A user (A,B and C have the same user)
        # A doesn't match anymore.
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000, topic=target_a.topic, user=target_a.user)
        target_c = TargetFactory(location=self.point_c, radius=30000, topic=target_a.topic, user=target_a.user)
        ChatFactory(target_one=target_a, target_two=target_b)
        ChatFactory(target_one=target_a, target_two=target_c)

        manage_target_chats(target_a)

        matches = len(list(target_a.get_matches()))
        chats_target_a = target_a.chat_one_set.count() + target_a.chat_two_set.count()
        self.assertEqual(matches, 0)
        self.assertEqual(chats_target_a, matches)

    def test_manage_target_chats_edit_target_topic(self):
        # Target A has A_B and A_C chats. After changing A topic (A,B and C have different topic)
        # A doesn't match anymore.
        target_a = TargetFactory(location=self.point_a, radius=50000)
        target_b = TargetFactory(location=self.point_b, radius=100000)
        target_c = TargetFactory(location=self.point_c, radius=30000)
        ChatFactory(target_one=target_a, target_two=target_b)
        ChatFactory(target_one=target_a, target_two=target_c)

        manage_target_chats(target_a)

        matches = len(list(target_a.get_matches()))
        chats_target_a = target_a.chat_one_set.count() + target_a.chat_two_set.count()
        self.assertEqual(matches, 0)
        self.assertEqual(chats_target_a, matches)
