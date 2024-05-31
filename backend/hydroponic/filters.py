import django_filters
from django_filters import OrderingFilter
from hydroponic.models import HydroponicMeasurement


class HydroponicMeasurementFilter(django_filters.FilterSet):
    created_at__gt = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gt"
    )
    created_at__gte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at__lt = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lt"
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    ph__gt = django_filters.NumberFilter(field_name="ph", lookup_expr="gt")
    ph__gte = django_filters.NumberFilter(field_name="ph", lookup_expr="gte")
    ph__lt = django_filters.NumberFilter(field_name="ph", lookup_expr="lt")
    ph__lte = django_filters.NumberFilter(field_name="ph", lookup_expr="lte")

    tds__gt = django_filters.NumberFilter(field_name="tds", lookup_expr="gt")
    tds__gte = django_filters.NumberFilter(field_name="tds", lookup_expr="gte")
    tds__lt = django_filters.NumberFilter(field_name="tds", lookup_expr="lt")
    tds__lte = django_filters.NumberFilter(field_name="tds", lookup_expr="lte")

    water_temperature__gt = django_filters.NumberFilter(
        field_name="water_temperature", lookup_expr="gt"
    )
    water_temperature__gte = django_filters.NumberFilter(
        field_name="water_temperature", lookup_expr="gte"
    )
    water_temperature__lt = django_filters.NumberFilter(
        field_name="water_temperature", lookup_expr="lt"
    )
    water_temperature__lte = django_filters.NumberFilter(
        field_name="water_temperature", lookup_expr="lte"
    )

    order_by = OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("ph", "ph"),
            ("water_temperature", "water_temperature"),
            ("tds", "tds"),
        ),
    )

    class Meta:
        model = HydroponicMeasurement
        fields = [
            "created_at",
            "ph",
            "tds",
            "water_temperature",
            "system_id",
            "order_by",
        ]
