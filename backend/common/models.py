from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from django.db import models


class DateTimeUUIDMixin(models.Model):
    id: uuid4 = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NutrientsMixin(models.Model):
    carb: Decimal = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat: Decimal = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    protein: Decimal = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    kcal: Decimal = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        abstract = True
