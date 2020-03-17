from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.IntegerChoices):
        GENDER_MALE = 1
        GENDER_FEMALE = 2
        GENDER_OTHER = 3

    gender = models.IntegerField(choices=Gender.choices)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']

    @property
    def is_staff(self):
        # All superusers are staff
        return self.is_superuser

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
