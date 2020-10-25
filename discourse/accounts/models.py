from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers.account_manager import CustomAccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    COUNTRIES = [("BY", "Belarus")]

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    first_name = models.CharField("First name", max_length=15)
    second_name = models.CharField("Second name", max_length=15)
    email = models.EmailField("E-mail", unique=True)
    date_of_birth = models.DateField("Date of birth")
    country = models.CharField("Country", max_length=25, choices=COUNTRIES)
    sex = models.CharField("Sex", max_length=2, choices=SEX_CHOICES)

    date_joined = models.DateTimeField(verbose_name="Date joined",
                                       default=timezone.now)
    is_admin = models.BooleanField(verbose_name="admin", default=False)
    is_active = models.BooleanField(verbose_name="active", default=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'date_of_birth','country',
                       'sex', 'password']

    # Custom model manager
    objects = CustomAccountManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.email

    def get_age(self):
        """Helps to find out the age of a user according to his date of
        birth."""
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
