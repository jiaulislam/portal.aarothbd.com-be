from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    ADMIN = "admin", "Admin"
    WHOLESELLER = "wholeseller", "Wholeseller"
    CUSTOMER = "customer", "Customer"
