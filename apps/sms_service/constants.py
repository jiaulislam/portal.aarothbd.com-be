from django.db.models import TextChoices


class SMSStatusChoice(TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    ERROR = "ERROR", "Error"
