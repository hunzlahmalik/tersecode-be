from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import User
from .constants import avatar_storage_path, COUNTRIES


class Profile(models.Model):
    """
    User profile model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", help_text="User profile")
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="Short bio")
    avatar = models.ImageField(
        upload_to=avatar_storage_path,
        default="avatars/default.png",
        null=True,
        blank=True,
        help_text="User image avatar"
    )
    github = models.URLField(max_length=200, null=True, blank=True, help_text="Github profile")
    linkedin = models.URLField(max_length=200, null=True, blank=True, help_text="Linkedin profile")
    country = models.CharField(max_length=2, null=True, blank=True, choices=COUNTRIES, help_text="Country")

    def __str__(self):
        return self.user.email

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
