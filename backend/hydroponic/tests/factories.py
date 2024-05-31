import factory.fuzzy
from hydroponic.models import HydroponicMeasurement
from hydroponic.models import HydroponicSystem


class HydroponicSystemFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("pystr")
    description = factory.Faker("pystr")
    user = factory.SubFactory("users.tests.factories.UserFactory")

    class Meta:
        model = HydroponicSystem


class HydroponicMeasurementFactory(factory.django.DjangoModelFactory):
    ph = factory.fuzzy.FuzzyDecimal(low=0, high=14, precision=1)
    water_temperature = factory.fuzzy.FuzzyDecimal(low=-20, high=150, precision=1)
    tds = factory.Faker("pyint", min_value=0, max_value=1250)
    system = factory.SubFactory(HydroponicSystemFactory)

    class Meta:
        model = HydroponicMeasurement
