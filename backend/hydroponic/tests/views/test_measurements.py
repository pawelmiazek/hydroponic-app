import datetime
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

    @pytest.mark.freeze_time("2024-05-31T10:25:00Z")
    def test_case_measurements_filter_by_create_at_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory
    ):
        date_now = datetime.datetime.now()
        hydroponic_measurement_factory(system__user=user)

        api_client.force_authenticate(user=user)
        response = api_client.get(
            self.ENDPOINT,
            {
                "created_at__gte": date_now.isoformat(),
                "created_at__lte": (date_now + datetime.timedelta(hours=4)).isoformat(),
            },
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1

        response = api_client.get(
            self.ENDPOINT,
            {
                "created_at__gt": date_now.isoformat(),
                "created_at__lte": (date_now + datetime.timedelta(hours=4)).isoformat(),
            },
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 0

        response = api_client.get(
            self.ENDPOINT,
            {
                "created_at__gt": (date_now - datetime.timedelta(hours=4)).isoformat(),
                "created_at__lt": (date_now + datetime.timedelta(hours=4)).isoformat(),
            },
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1

    @pytest.mark.parametrize(
        "params, results_count",
        [
            ({"ph__gte": 7, "ph__lte": 10}, 1),
            ({"ph__gt": 7, "ph__lte": 10}, 0),
            ({"ph__gt": 4, "ph__lt": 8}, 1),
        ],
    )
    def test_case_measurements_filter_by_ph_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory, params, results_count
    ):
        hydroponic_measurement_factory(system__user=user, ph=7)

        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT, params)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == results_count

    @pytest.mark.parametrize(
        "params, results_count",
        [
            ({"tds__gte": 125, "tds__lte": 150}, 1),
            ({"tds__gt": 125, "tds__lte": 150}, 0),
            ({"tds__gt": 100, "tds__lt": 130}, 1),
        ],
    )
    def test_case_measurements_filter_by_tds_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory, params, results_count
    ):
        hydroponic_measurement_factory(system__user=user, tds=125)

        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT, params)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == results_count

    @pytest.mark.parametrize(
        "params, results_count",
        [
            ({"water_temperature__gte": 21, "water_temperature__lte": 30}, 1),
            ({"water_temperature__gt": 21, "water_temperature__lte": 30}, 0),
            ({"water_temperature__gt": -10, "water_temperature__lt": 25}, 1),
        ],
    )
    def test_case_measurements_filter_by_temperature_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory, params, results_count
    ):
        hydroponic_measurement_factory(system__user=user, water_temperature=21)

        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT, params)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == results_count

    def test_case_measurements_filter_by_system_id_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory
    ):
        measurement = hydroponic_measurement_factory(system__user=user)
        measurement_2 = hydroponic_measurement_factory()

        api_client.force_authenticate(user=user)
        response = api_client.get(
            self.ENDPOINT, {"system_id": str(measurement.system.id)}
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1

        response = api_client.get(
            self.ENDPOINT, {"system_id": str(measurement_2.system.id)}
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 0

    def test_case_measurements_order_by_ph_return_filtered_list(
        self, api_client, user, hydroponic_measurement_factory
    ):
        measurement = hydroponic_measurement_factory(system__user=user, ph=6)
        measurement_2 = hydroponic_measurement_factory(system__user=user, ph=8)

        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT, {"order_by": "ph"})

        assert response.status_code == status.HTTP_200_OK
        assert [m["id"] for m in response.json()["results"]] == [
            str(measurement.id),
            str(measurement_2.id),
        ]

        response = api_client.get(self.ENDPOINT, {"order_by": "-ph"})

        assert response.status_code == status.HTTP_200_OK
        assert [m["id"] for m in response.json()["results"]] == [
            str(measurement_2.id),
            str(measurement.id),
        ]

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
