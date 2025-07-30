from django.db import models

from core.models import BaseModel


class UoMTypeChoices(models.TextChoices):
    BIGGER = "bigger", "Bigger"
    SMALLER = "smaller", "Smaller"
    REFERENCE = "reference", "Reference"


class UoMCategory(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "uom_uom_category"
        verbose_name_plural = "UoM Categories"
        verbose_name = "UoM Category"

    def __str__(self) -> str:
        return self.name


class UoM(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Unit of Measure")
    category = models.ForeignKey(
        UoMCategory,
        on_delete=models.PROTECT,
        verbose_name="Unit of Measure Category",
        help_text="Conversion between Units of Measure can only occur if they belong to the same category."
        "The conversion will be made based on the ratios.",
        null=True,
        blank=True,
    )
    ratio = models.FloatField(
        verbose_name="Ratio",
        default=1.0,
        blank=False,
        null=False,
        help_text=(
            "How much bigger or smaller this unit is compared to the reference Unit "
            "of Measure for this category: 1 * (reference unit) = ratio * (this unit)"
        ),
    )

    uom_type = models.CharField(
        max_length=100,
        verbose_name="Unit of Measure Type",
        choices=UoMTypeChoices.choices,
        default=UoMTypeChoices.REFERENCE,
    )

    class Meta:
        db_table = "uom_uom"
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Unit of Measures"

    def __str__(self) -> str:
        return self.name
