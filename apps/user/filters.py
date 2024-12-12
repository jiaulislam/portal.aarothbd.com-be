from django.contrib.auth import get_user_model
from django_filters import OrderingFilter

from core.filter import BaseFilter

User = get_user_model()

class UserFilterSet(BaseFilter):

    order_by = OrderingFilter(
        fields=(
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
            ('company__name', 'company'),
        ),

        field_labels={
            "first_name": "First Name",
            "last_name": "Last Name",
            "company__name": "Company",
        }
    )

    class Meta:
        model = User
        exclude = ("password", "date_joined", "last_login", "user_permissions", "groups")
