from django.apps import AppConfig


class CustomerOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.customer_order"
    verbose_name = "Customer Order"
    verbose_name_plural = "Customer Orders"
