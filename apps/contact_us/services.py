from django.conf import settings
from django.core.mail import EmailMessage

from core.services import BaseModelService
from core.services.sentry_service import capture_exception_sentry

from .models import EmailRecepient


class EmailReceipentService(BaseModelService[EmailRecepient]):
    model_class = EmailRecepient

    def send_email(self, subject, message):
        email_receipent = self.all().first()
        try:
            if email_receipent:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_receipent.to_email],
                    cc=email_receipent.cc_email,
                    bcc=email_receipent.bcc_email,
                )
                email.send()
                return True
            return False
        except Exception as e:
            capture_exception_sentry(e)
            return False
