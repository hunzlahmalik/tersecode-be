from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        "email address",
        unique=True,
        help_text=_("Required. Inform a valid email address."),
        error_messages={
            "unique": _("A users with that email already exists."),
        },
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this users should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-id"]
