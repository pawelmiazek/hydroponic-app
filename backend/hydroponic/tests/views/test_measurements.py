from decimal import Decimal

import pytest
from hydroponic.models import HydroponicMeasurement
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestHydroponicSystemViewSet:
    ENDPOINT: str = "/hydroponic/measurements/"

    def test_case_not_authorized_return_error(self, api_client):
        response = api_client.get(self.ENDPOINT)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_case_no_systems_return_empty_list(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert result == []

    def test_case_measurements_return_list(
        self, api_client, user, hydroponic_measurement_factory
    ):
        measurements = hydroponic_measurement_factory.create_batch(2, system__user=user)
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        assert {str(measurement.id) for measurement in measurements} == {
            measurement["id"] for measurement in result
        }

    def test_case_measurements_for_user_return_filtered_list(
        self, api_client, hydroponic_measurement_factory
    ):
        measurements = hydroponic_measurement_factory.create_batch(3)
        user = measurements[0].system.user
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1
        assert {
            str(measurement.id)
            for measurement in HydroponicMeasurement.objects.filter(system__user=user)
        } == {measurement["id"] for measurement in result}

    def test_case_create_measurement_return_success_data(
        self, api_client, hydroponic_system
    ):
        api_client.force_authenticate(user=hydroponic_system.user)
        ph_value = Decimal("7.5")
        temperature_value = Decimal("22.3")
        tds_value = 180

        response = api_client.post(
            self.ENDPOINT,
            {
                "system_id": str(hydroponic_system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert HydroponicMeasurement.objects.filter(
            id=result["id"],
            ph=ph_value,
            water_temperature=temperature_value,
            tds=tds_value,
        ).exists()

    def test_case_create_measurement_with_negative_ph_return_error(
        self, api_client, hydroponic_system
    ):
        api_client.force_authenticate(user=hydroponic_system.user)
        ph_value = Decimal("-7.5")
        temperature_value = Decimal("22.3")
        tds_value = 180

        response = api_client.post(
            self.ENDPOINT,
            {
                "system_id": str(hydroponic_system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ensure this value is greater than or equal to 0." in result["ph"]

    def test_case_create_measurement_with_too_big_ph_return_error(
        self, api_client, hydroponic_system
    ):
        api_client.force_authenticate(user=hydroponic_system.user)
        ph_value = Decimal("15.5")
        temperature_value = Decimal("22.3")
        tds_value = 180

        response = api_client.post(
            self.ENDPOINT,
            {
                "system_id": str(hydroponic_system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ensure this value is less than or equal to 14." in result["ph"]

    def test_case_create_measurement_with_negative_tds_return_error(
        self, api_client, hydroponic_system
    ):
        api_client.force_authenticate(user=hydroponic_system.user)
        ph_value = Decimal("7.5")
        temperature_value = Decimal("22.3")
        tds_value = -180

        response = api_client.post(
            self.ENDPOINT,
            {
                "system_id": str(hydroponic_system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ensure this value is greater than or equal to 0." in result["tds"]

    def test_case_create_measurement_with_not_owned_system_return_error(
        self, api_client, user, hydroponic_system_factory
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory()
        ph_value = Decimal("7.5")
        temperature_value = Decimal("22.3")
        tds_value = 180

        response = api_client.post(
            self.ENDPOINT,
            {
                "system_id": str(system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Hydroponic system not found." in result["system_id"]

    def test_update_measurement_return_error(self, api_client, hydroponic_measurement):
        api_client.force_authenticate(user=hydroponic_measurement.system.user)
        ph_value = Decimal("7.5")
        temperature_value = Decimal("22.3")
        tds_value = 180

        response = api_client.patch(
            f"{self.ENDPOINT}{hydroponic_measurement.id}/",
            {
                "system_id": str(hydroponic_measurement.system.id),
                "ph": ph_value,
                "water_temperature": temperature_value,
                "tds": tds_value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_system_then_properly_remove(
        self, api_client, hydroponic_measurement
    ):
        api_client.force_authenticate(user=hydroponic_measurement.system.user)
        response = api_client.delete(f"{self.ENDPOINT}{hydroponic_measurement.id}/")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
