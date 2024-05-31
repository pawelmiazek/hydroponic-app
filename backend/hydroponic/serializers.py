from collections import OrderedDict

from common.decorators import context_user_required
from django.utils.translation import gettext_lazy as _
from hydroponic.models import HydroponicMeasurement
from hydroponic.models import HydroponicSystem
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class MeasurementsForSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicMeasurement
        fields = ("id", "ph", "water_temperature", "tds")


@context_user_required
class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = ("id", "name", "description")

    def create(self, validated_data: OrderedDict, **kwargs) -> HydroponicSystem:
        return HydroponicSystem.objects.create(user=self.context_user, **validated_data)


@context_user_required
class HydroponicSystemDetailsSerializer(serializers.ModelSerializer):
    measurements = serializers.SerializerMethodField()

    class Meta:
        model = HydroponicSystem
        fields = ("id", "name", "description", "measurements")

    def get_measurements(self, obj: HydroponicSystem) -> HydroponicMeasurement:
        measurements = obj.measurements.all().order_by("-created_at")[:10]
        return MeasurementsForSystemSerializer(measurements, many=True).data


@context_user_required
class HydroponicMeasurementSerializer(serializers.ModelSerializer):
    system_id = serializers.PrimaryKeyRelatedField(
        queryset=HydroponicSystem.objects.all(), write_only=True
    )
    system = HydroponicSystemSerializer(read_only=True)

    default_error_messages = {"invalid_system": _("Hydroponic system not found.")}

    class Meta:
        model = HydroponicMeasurement
        fields = ("id", "system_id", "system", "ph", "water_temperature", "tds")

    def validate_system_id(
        self, value: HydroponicSystem
    ) -> HydroponicSystem | ValidationError:
        if value.user != self.context_user:
            self.fail("invalid_system")

        return value

    def create(self, validated_data: OrderedDict, **kwargs) -> HydroponicSystem:
        system = validated_data.pop("system_id")
        return HydroponicMeasurement.objects.create(system=system, **validated_data)
