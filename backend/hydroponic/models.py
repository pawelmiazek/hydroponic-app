from decimal import Decimal
from typing import TYPE_CHECKING

from common.models import DateTimeUUIDMixin
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

if TYPE_CHECKING:
    from users.models import User


class HydroponicSystem(DateTimeUUIDMixin):
    name: str = models.CharField(max_length=150, unique=True)
    description: str = models.TextField(null=True, blank=True)
    user: "User" = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="hydroponic_systems"
    )

    class Meta:
        verbose_name = "HydroponicSystem"
        verbose_name_plural = "HydroponicSystems"

    def __str__(self) -> str:
        return self.name


class HydroponicMeasurement(DateTimeUUIDMixin):
    system: HydroponicSystem = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
    )
    ph: int = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(14),
        ],
    )
    water_temperature: Decimal = models.DecimalField(
        max_digits=4, decimal_places=1
    )  # Unit: Celsius degrees
    tds: int = models.PositiveSmallIntegerField()  # Unit: ppm

    class Meta:
        verbose_name = "HydroponicMeasurement"
        verbose_name_plural = "HydroponicMeasurements"
