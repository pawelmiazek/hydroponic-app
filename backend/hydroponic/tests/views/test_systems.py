import pytest
from hydroponic.models import HydroponicSystem
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestHydroponicSystemViewSet:
    ENDPOINT: str = "/hydroponic/systems/"

    def test_case_not_authorized_return_error(self, api_client):
        response = api_client.get(self.ENDPOINT)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_case_no_systems_return_empty_list(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert result == []

    def test_case_systems_return_list(
        self, api_client, user, hydroponic_system_factory
    ):
        systems = hydroponic_system_factory.create_batch(2, user=user)
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        assert {str(system.id) for system in systems} == {
            system["id"] for system in result
        }

    def test_case_systems_for_user_return_filtered_list(
        self, api_client, hydroponic_system_factory
    ):
        systems = hydroponic_system_factory.create_batch(3)
        user = systems[0].user
        api_client.force_authenticate(user=user)

        response = api_client.get(self.ENDPOINT)
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1
        assert {str(system.id) for system in user.hydroponic_systems.all()} == {
            system["id"] for system in result
        }
        assert not hasattr(result[0], "measurements")

    def test_case_systems_filter_by_name_return_filtered_list(
        self, api_client, user, hydroponic_system_factory
    ):
        hydroponic_system_factory.create_batch(2)
        hydroponic_system_factory.create_batch(2, user=user, name="Test system")
        hydroponic_system_factory(user=user, name="Test system 2")

        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT, {"search": "Test system"})
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 3

        response = api_client.get(self.ENDPOINT, {"search": "Test system 2"})
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 1

        response = api_client.get(
            self.ENDPOINT, {"search": "Definietely not system name"}
        )
        result = response.json()["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 0

    def test_case_create_system_return_success_data(self, api_client, user):
        api_client.force_authenticate(user=user)
        system_name = "Test system"

        response = api_client.post(
            self.ENDPOINT,
            {
                "name": system_name,
                "description": "Test system's description",
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert HydroponicSystem.objects.filter(
            id=result["id"], name=system_name
        ).exists()

    def test_update_system_return_proper_data(
        self, api_client, user, hydroponic_system_factory
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory(user=user)
        system_name = "Test system"

        response = api_client.patch(
            f"{self.ENDPOINT}{system.id}/",
            {
                "name": system_name,
                "description": "Test system's description",
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        system = HydroponicSystem.objects.filter(id=result["id"]).first()
        assert system.name == system_name

    def test_update_not_owned_system_return_error(
        self, api_client, user, hydroponic_system_factory
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory()
        system_name = "Test system"

        response = api_client.patch(
            f"{self.ENDPOINT}{system.id}/",
            {
                "name": system_name,
                "description": "Test system's description",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_system_return_proper_data(
        self,
        api_client,
        user,
        hydroponic_system_factory,
        hydroponic_measurement_factory,
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory(user=user)
        hydroponic_measurement_factory.create_batch(15, system=system)

        response = api_client.get(f"{self.ENDPOINT}{system.id}/")
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["id"] == str(system.id)
        assert result["name"] == system.name
        assert result["description"] == system.description
        assert len(result["measurements"]) == 10

    def test_delete_system_then_properly_remove(
        self, api_client, user, hydroponic_system_factory
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory(user=user)

        response = api_client.delete(f"{self.ENDPOINT}{system.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not HydroponicSystem.objects.filter(id=system.id).exists()

    def test_delete_not_owned_system_then_return_error(
        self, api_client, user, hydroponic_system_factory
    ):
        api_client.force_authenticate(user=user)
        system = hydroponic_system_factory()

        response = api_client.delete(f"{self.ENDPOINT}{system.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert HydroponicSystem.objects.filter(id=system.id).exists()
