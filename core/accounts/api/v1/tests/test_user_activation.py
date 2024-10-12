from django.urls import reverse

import pytest

from ...utils import create_token


@pytest.mark.django_db
def test_activation_with_valid_token(client, user):
    token = create_token("user_id", user.id)
    assert not user.is_verified
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("Message")
    assert response.status_code == 200
    assert response_data == "your account has been activated."
    user.refresh_from_db()
    assert user.is_verified


@pytest.mark.django_db
def test_activation_for_active_user_with_valid_token(client, active_user):
    token = create_token("user_id", active_user.id)
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("Message")
    assert response.status_code == 400
    assert response_data == "your account has already been activated !!!"


@pytest.mark.django_db
def test_activation_for_user_with_invalid_token(client, user):
    token = create_token("user_id", user.id)
    token += "test"
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("Message")
    assert response.status_code == 400
    assert response_data == "Token is invalid or expired"


@pytest.mark.django_db
def test_activation_for_active_user_with_invalid_token(client, active_user):
    token = create_token("user_id", active_user.id)
    token += "test"
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("Message")
    assert response.status_code == 400
    assert response_data == "Token is invalid or expired"


@pytest.mark.django_db
def test_activation_for_unavailable_user_with_valid_token(client):
    token = create_token("user_id", 99)
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No User matches the given query."


@pytest.mark.django_db
def test_activation_for_unavailable_user_with_invalid_token(client):
    token = create_token("user_id", 99)
    token += "test"
    url = reverse("account:api-v1:activation", kwargs={"token": token})
    response = client.get(path=url)
    response_data = response.data.get("Message")
    assert response.status_code == 400
    assert response_data == "Token is invalid or expired"


@pytest.mark.django_db
def test_activation_resend_for_user_with_valid_email(client, user):
    user_email = user.email
    url = reverse("account:api-v1:activation-resend")
    response = client.post(path=url, data={"email": user_email})
    response_data = response.data.get("detail")
    assert response.status_code == 200
    assert response_data == f"an activation email has been sent to {user_email} Again"


@pytest.mark.django_db
def test_activation_resend_for_active_user_with_valid_email(client, active_user):
    user_email = active_user.email
    url = reverse("account:api-v1:activation-resend")
    response = client.post(path=url, data={"email": user_email})
    response_data = response.data.get("detail")
    assert response.status_code == 400
    assert response_data == "your account has already been activated !!!"


@pytest.mark.django_db
def test_activation_resend_for_user_with_invalid_email(client):
    user_email = "123"
    url = reverse("account:api-v1:activation-resend")
    response = client.post(path=url, data={"email": user_email})
    response_data = response.data.get("email")[0]
    assert response.status_code == 400
    assert response_data == "Enter a valid email address."


@pytest.mark.django_db
def test_activation_resend_for_unavailable_user(client):
    user_email = "test@mail.com"
    url = reverse("account:api-v1:activation-resend")
    response = client.post(path=url, data={"email": user_email})
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No User matches the given query."
