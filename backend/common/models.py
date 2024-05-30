from datetime import datetime
from uuid import uuid4

from django.db import models


class DateTimeUUIDMixin(models.Model):
    id: uuid4 = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
