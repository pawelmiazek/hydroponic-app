from django.contrib import admin
from hydroponic.models import HydroponicMeasurement
from hydroponic.models import HydroponicSystem


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = ("user",)
    search_fields = (
        "user__email",
        "name",
    )
    readonly_fields = ("user",)


@admin.register(HydroponicMeasurement)
class HydroponicMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "system",
        "ph",
        "water_temperature",
        "tds",
        "created_at",
        "updated_at",
    )
    list_filter = ("system", "system__user")
    search_fields = (
        "system__name",
        "system__user__email",
    )
    readonly_fields = (
        "ph",
        "water_temperature",
        "tds",
    )
