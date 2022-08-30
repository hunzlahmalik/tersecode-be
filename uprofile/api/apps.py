from django.apps import AppConfig


class UserProfileAPIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "uprofile.api"
    verbose_name = "User Profile API"
    verbose_name_plural = "User Profile API"
    label = "uprofile_api"
