from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from profile.managers import UserManager
from profile.models import User


class UserManagerTestCase(TestCase):

    def setUp(self):
        self.manager = UserManager()
        self.manager.model = get_user_model()

    def test_can_create_user_ok(self):
        user = self.manager.create_user("test@test.com", "password1234", gender=User.Gender.GENDER_MALE)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.gender, User.Gender.GENDER_MALE)
        self.assertFalse(user.is_staff)

    def test_can_create_user_empty_email(self):
        self.assertRaises(ValueError, self.manager.create_user, email="", password="test1234", gender=2)

    def test_can_create_user_without_gender(self):
        self.assertRaises(IntegrityError, self.manager.create_user, email="test@test.com", password="test1234")

    def test_can_create_superuser_ok(self):
        user = self.manager.create_superuser("test@test.com", "password1234", gender=User.Gender.GENDER_FEMALE)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.gender, User.Gender.GENDER_FEMALE)
        self.assertTrue(user.is_staff)

    def test_can_create_superuser_false_is_superuser_flag(self):
        self.assertRaises(ValueError,
                          self.manager.create_superuser,
                          email="test@test.com",
                          password="test1234",
                          is_superuser=False,
                          gender=2)
