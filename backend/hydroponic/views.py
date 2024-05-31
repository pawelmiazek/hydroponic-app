from hydroponic.filters import HydroponicMeasurementFilter
from hydroponic.models import HydroponicMeasurement
from hydroponic.models import HydroponicSystem
from hydroponic.serializers import HydroponicMeasurementSerializer
from hydroponic.serializers import HydroponicSystemDetailsSerializer
from hydroponic.serializers import HydroponicSystemSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            # fyi: https://github.com/axnsan12/drf-yasg/issues/333
            return HydroponicSystem.objects.none()

        return (
            HydroponicSystem.objects.filter(user=self.request.user)
            .prefetch_related("measurements")
            .order_by("id")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return HydroponicSystemDetailsSerializer

        return HydroponicSystemSerializer


class HydroponicMeasurementViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = HydroponicMeasurement.objects.all()
    serializer_class = HydroponicMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = HydroponicMeasurementFilter

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
