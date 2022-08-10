from django.db import models
from django.contrib.auth.models import AbstractUser

from account.constants import COUNTRIES, AVATAR_STORAGE_PATH


class User(AbstractUser):

    # overiding
    email = models.EmailField("email address", unique=True)

    # new fields
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to=AVATAR_STORAGE_PATH,
                               default='avatars/default.png', null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    country = models.CharField(
        max_length=2, null=True, blank=True, choices=COUNTRIES)

    REQUIRED_FIELDS = ['email']
