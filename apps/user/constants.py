from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    CENTRAL_ADMIN = "central_admin", "Central Admin"
    WHOLESELLER = "wholeseller", "Wholeseller"
    CUSTOMER = "customer", "Customer"
