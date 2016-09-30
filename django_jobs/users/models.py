from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models

from rest_framework.authtoken.models import Token


class AppUserManager(BaseUserManager):
    """
    Customer manager class for custom user model
    """
    def create_user(self, email, password=None, **kwargs):
        """
        Custom method to use when creating users
        """
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        Token.objects.get_or_create(user=user)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(
            email, password, **kwargs
        )

        user.is_staff = user.is_superuser = True
        user.save()

        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for app users. Used to
    store profile details and for payments.
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered"
                                 " in the format: '+999999999'. Up to"
                                 " 15 digits allowed.")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    college = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(validators=[phone_regex], blank=True,
                              max_length=15)
    college_year = models.PositiveIntegerField(null=True, default=1)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False,
                                     help_text="Whether this user subscribed"
                                               " to a paid plan")

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = AppUserManager()

    def get_short_name(self):
        if self.first_name:
            return u"%s" % self.first_name

        return ""

    def get_full_name(self):
        if not (self.first_name or self.last_name):
            return ""

        return u"%s %s" % (self.first_name + self.last_name)

    def __unicode__(self):
        return u"%s" % self.email
