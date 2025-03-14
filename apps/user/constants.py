from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    CENTRAL_ADMIN = "central_admin", "Central Admin"
    WHOLESELLER_ADMIN = "wholeseller_admin", "Wholeseller Admin"
    CUSTOMER = "customer", "Customer"


class AuthProviderChoices(TextChoices):
    FACEBOOK = "facebook", "Facebook"
    GOOGLE = "google", "Google"
    EMAIL = "email", "Email"
    USERNAME = "user_name", "Username"
