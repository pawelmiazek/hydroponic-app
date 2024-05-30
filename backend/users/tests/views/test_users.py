import pytest
from rest_framework import status
from users.models import User

pytestmark = pytest.mark.django_db


class TestRegisterViewSet:
    ENDPOINT: str = "/auth/users/register/"

    def test_case_no_data_then_return_400(self, api_client):
        response = api_client.post(self.ENDPOINT, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_case_proper_data_then_create_user(self, api_client, mocker, faker):
        email, password = faker.email(), faker.pystr(max_chars=12)
        response = api_client.post(
            self.ENDPOINT, {"email": email, "password": password}, format="json"
        )
        result = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert result == {"id": mocker.ANY, "email": email}
        assert User.objects.filter(email=email).exists()


class TestCurrentUserView:
    ENDPOINT: str = "/auth/users/current_user/"

    def test_case_not_authorized_return_error(self, api_client):
        response = api_client.get(self.ENDPOINT)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_case_authorized_return_proper_data(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.ENDPOINT)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["id"] == str(user.id)
        assert result["email"] == user.email
