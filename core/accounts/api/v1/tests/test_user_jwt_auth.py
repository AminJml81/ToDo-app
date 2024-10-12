from django.urls import reverse

import pytest

from ...utils import decode_token


@pytest.mark.django_db
def test_create_jwt_tokens_with_username(client, active_user):
    username_email, password = active_user.username, "testpassword123"
    url = reverse("account:api-v1:jwt-create")
    data = {"username_email": username_email, "password": password}
    response = client.post(path=url, data=data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

    # testing token
    access_token, refresh_token = response.data.get("access"), response.data.get(
        "refresh"
    )
    decoded_access_token = decode_token(access_token, "user_id")
    decoded_refresh_token = decode_token(refresh_token, "user_id")
    assert decoded_access_token == decoded_refresh_token == 1


@pytest.mark.django_db
def test_create_pair_jwt_tokens_with_email(client, active_user):
    username_email, password = active_user.email, "testpassword123"
    url = reverse("account:api-v1:jwt-create")
    data = {"username_email": username_email, "password": password}
    response = client.post(path=url, data=data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

    access_token, refresh_token = response.data.get("access"), response.data.get(
        "refresh"
    )
    decoded_access_token = decode_token(access_token, "user_id")
    decoded_refresh_token = decode_token(refresh_token, "user_id")
    assert decoded_access_token == decoded_refresh_token == 1


@pytest.mark.parametrize(
    "username_email, password",
    [
        ("testt", "testpassword123"),  # no user with this username.
        ("testt@mail.com", "testpassword123"),  # no user with this email.
        ("test", "testpassword321"),  # correct username but incorrect password.
        ("test@mail.com", "testpassword321"),  # correct email but incorrect password.
    ],
)
@pytest.mark.django_db
def test_create_pair_jwt_tokens_with_invalid_credentials(
    client, username_email, password
):
    url = reverse("account:api-v1:jwt-create")
    data = {"username_email": username_email, "password": password}
    response = client.post(path=url, data=data)
    response_data = response.data.get("credentials error")[0]
    assert response.status_code == 400
    assert response_data == "Unable to log in with provided credentials."


@pytest.mark.django_db
def test_jwt_refresh_with_valid_token(client, jwt_refresh_token):
    url = reverse("account:api-v1:jwt-refresh")
    data = {
        "refresh": jwt_refresh_token,
    }
    response = client.post(path=url, data=data)
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_jwt_refresh_with_invalid_token(client, jwt_refresh_token):
    url = reverse("account:api-v1:jwt-refresh")
    jwt_refresh_token += "bad"
    data = {
        "refresh": jwt_refresh_token,
    }
    response = client.post(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Token is invalid or expired"


@pytest.mark.django_db
def test_verify_jwt_with_valid_token(client, jwt_access_token):
    url = reverse("account:api-v1:token-verify")
    data = {
        "token": jwt_access_token,
    }
    response = client.post(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 200
    assert response_data is None


@pytest.mark.django_db
def test_verify_jwt_with_invalid_token(client, jwt_access_token):
    url = reverse("account:api-v1:token-verify")
    jwt_access_token += "bad"
    data = {
        "token": jwt_access_token,
    }
    response = client.post(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Token is invalid or expired"
