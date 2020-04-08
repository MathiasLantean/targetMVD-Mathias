import factory

from profile.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'userTest%d@test.com' % n)
    gender = factory.Faker('random_element', elements=[x[0] for x in User.Gender.choices])
    password = factory.PostGenerationMethodCall('set_password', 'defaultPassword')


class AdminUserFactory(UserFactory):
    is_superuser = True


class CommonUserFactory(UserFactory):
    is_superuser = False


class InactiveUserFactory(UserFactory):
    is_active = False
