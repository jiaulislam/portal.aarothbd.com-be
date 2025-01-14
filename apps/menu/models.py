from django.contrib.auth.models import Group
from django.db import models

from core.models import BaseModel


class NavMenu(BaseModel):
    code_name = models.CharField(max_length=255, verbose_name="Code Name", unique=True)
    view_name = models.CharField(max_length=255, verbose_name="View Name")
    icon = models.TextField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="nav_menus", blank=True)
    parent_menu = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="child_menus"
    )
    order = models.IntegerField(default=1)

    child_menus: models.QuerySet["NavMenu"]

    class Meta:
        db_table = "menu_menu"
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"
        ordering = ["order"]

    def __str__(self) -> str:
        return self.view_name
