from hydroponic.views import HydroponicMeasurementViewSet
from hydroponic.views import HydroponicSystemViewSet
from rest_framework.routers import DefaultRouter


app_name = "hydroponic"

router = DefaultRouter()
router.register(r"systems", HydroponicSystemViewSet, basename="systems")
router.register(r"measurements", HydroponicMeasurementViewSet, basename="measurements")

urlpatterns = router.urls
