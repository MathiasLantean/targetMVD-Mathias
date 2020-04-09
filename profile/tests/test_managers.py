from django.contrib.auth import get_user_model
from django.test import TestCase
from profile.managers import UserManager
from profile.models import User


class UserManagerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test@test.com'
        cls.user_password = 'test123455'
        cls.user_first_name = 'user_test_name'
        cls.user_last_name = 'user_test_last_name'

    def setUp(self):
        self.manager = UserManager()
        self.manager.model = get_user_model()

    def test_can_create_user_ok(self):
        user = self.manager.create_user(
            self.user_email,
            self.user_password,
            first_name=self.user_first_name,
            last_name=self.user_last_name,
            gender=User.Gender.GENDER_MALE,
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_email)
        self.assertEqual(user.gender, User.Gender.GENDER_MALE)
        self.assertFalse(user.is_staff)
        self.assertEqual(f'{self.user_first_name} {self.user_last_name}', user.get_full_name())

    def test_can_create_user_empty_email(self):
        self.assertRaises(ValueError, self.manager.create_user, email="", password=self.user_password, gender=2)

    def test_can_create_user_without_gender(self):
        user = self.manager.create_user(self.user_email, self.user_password)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_email)
        self.assertIsNone(user.gender)
        self.assertFalse(user.is_staff)

    def test_can_create_superuser_ok(self):
        user = self.manager.create_superuser(self.user_email, self.user_password, gender=User.Gender.GENDER_FEMALE)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_email)
        self.assertEqual(user.gender, User.Gender.GENDER_FEMALE)
        self.assertTrue(user.is_staff)

    def test_can_create_superuser_false_is_superuser_flag(self):
        self.assertRaises(
            ValueError,
            self.manager.create_superuser,
            email=self.user_email,
            password="test1234",
            is_superuser=False,
            gender=User.Gender.GENDER_FEMALE
        )
