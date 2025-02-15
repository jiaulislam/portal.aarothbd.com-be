from django.apps import AppConfig


class SocialAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.social_auth"
    verbose_name = "Social Auth Provider"
    verbose_name_plural = "Social Auth Providers"
