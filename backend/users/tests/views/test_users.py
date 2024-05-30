import pytest
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
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


class TestObtainTokenPairView:
    ENDPOINT = "/auth/token/"

    def test_case_wrong_data_then_fail(self, api_client, user):
        response = api_client.post(
            self.ENDPOINT,
            {"email": user.email, "password": "wrong guess"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_case_data_correct_then_return_tokens(self, api_client, user, mocker):
        user.set_password("test_pass")
        user.save()
        user = User.objects.get(email=user.email)

        response = api_client.post(
            self.ENDPOINT,
            {
                "email": user.email,
                "password": "test_pass",
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["access"] == mocker.ANY
        assert result["refresh"] == mocker.ANY

        auth = JWTAuthentication()
        token = auth.get_validated_token(result["access"])
        assert auth.get_user(token) == user


class TestRefreshTokenView:
    ENDPOINT = "/auth/token/refresh/"

    def test_case_wrong_data_then_fail(self, api_client):
        response = api_client.post(
            self.ENDPOINT,
            {
                "refresh": "wrong_token",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_case_data_correct_then_return_tokens(self, api_client, user, mocker):
        token = RefreshToken.for_user(user)

        response = api_client.post(
            self.ENDPOINT,
            {
                "refresh": str(token),
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["access"] == mocker.ANY

        auth = JWTAuthentication()
        token = auth.get_validated_token(result["access"])
        assert auth.get_user(token) == user


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
