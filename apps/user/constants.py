from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    CENTRAL_ADMIN = "central_admin", "Central Admin"
    WHOLESELLER_ADMIN = "wholeseller_admin", "Wholeseller Admin"
    CUSTOMER = "customer", "Customer"
