from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

from .manager import UserManager


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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "user_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def full_name(self) -> str:
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "user_user_profile"
        verbose_name = "user_profile"
        verbose_name_plural = "user_profiles"

    def __str__(self):
        return "{} - {}".format(str(self.pk), self.user.email)
