from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

from .constants import AuthProviderChoices, UserTypeChoices
from .manager import UserManager

if TYPE_CHECKING:
    from wishlist.models import Wishlist


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(_("First Name"), max_length=88, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=88, null=True, blank=True)
    is_admin = models.BooleanField(
        _("Admin Status"),
        default=False,
        help_text=_("Designates that this user has all permissions but not as same superuser."),
    )
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    user_type = models.CharField(max_length=55, choices=UserTypeChoices.choices, default=UserTypeChoices.CUSTOMER)
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        related_name="company_users",
        null=True,
        blank=True,
    )
    auth_provider = models.CharField(
        max_length=120,
        choices=AuthProviderChoices.choices,
        default=AuthProviderChoices.EMAIL,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    profile: "UserProfile"
    wishlist: "Wishlist"

    class Meta:
        db_table = "user_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self) -> None:
        super().clean()
        self.email = BaseUserManager.normalize_email(self.email)

    @property
    def full_name(self) -> str:
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str | None:
        if self.first_name:
            return self.first_name
        return None

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_central_admin(self) -> bool:
        return self.user_type == UserTypeChoices.CENTRAL_ADMIN.value

    @property
    def is_tenant(self) -> bool:
        return self.user_type == UserTypeChoices.WHOLESELLER_ADMIN.value

    @property
    def is_customer(self) -> bool:
        return self.user_type == UserTypeChoices.CUSTOMER.value

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, null=True, blank=True)
    bin_id = models.CharField(max_length=88, null=True, blank=True)
    tin_id = models.CharField(max_length=88, null=True, blank=True)
    emergency_contact_details = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "user_user_profile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return "{} - {}".format(str(self.pk), self.user.email)
