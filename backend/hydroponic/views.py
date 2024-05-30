from hydroponic.models import HydroponicMeasurement
from hydroponic.models import HydroponicSystem
from hydroponic.serializers import HydroponicMeasurementSerializer
from hydroponic.serializers import HydroponicSystemSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            # fyi: https://github.com/axnsan12/drf-yasg/issues/333
            return HydroponicSystem.objects.none()

        return HydroponicSystem.objects.filter(user=self.request.user).order_by("id")


class HydroponicMeasurementViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = HydroponicMeasurement.objects.all()
    serializer_class = HydroponicMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            # fyi: https://github.com/axnsan12/drf-yasg/issues/333
            return HydroponicMeasurement.objects.none()

        return (
            HydroponicMeasurement.objects.filter(system__user=self.request.user)
            .select_related("system")
            .order_by("-created_at")
        )
