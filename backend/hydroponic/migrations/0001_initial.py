# Generated by Django 4.1 on 2024-05-30 14:18
import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HydroponicSystem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hydroponic_systems",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "HydroponicSystem",
                "verbose_name_plural": "HydroponicSystems",
            },
        ),
        migrations.CreateModel(
            name="HydroponicMeasurement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "ph",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(14),
                        ],
                    ),
                ),
                (
                    "water_temperature",
                    models.DecimalField(decimal_places=1, max_digits=4),
                ),
                ("tds", models.PositiveSmallIntegerField()),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="measurements",
                        to="hydroponic.hydroponicsystem",
                    ),
                ),
            ],
            options={
                "verbose_name": "HydroponicMeasurement",
                "verbose_name_plural": "HydroponicMeasurements",
            },
        ),
    ]
