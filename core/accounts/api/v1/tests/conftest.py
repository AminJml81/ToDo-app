import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from ....models import User
from ...utils import create_token


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture()
def user():
    user = User.objects.create_user(
        username = 'test', 
        email = 'test@mail.com',
        password = 'testpassword123',
    )
    return user

@pytest.fixture()
def active_user():
    user = User.objects.create_user(
        username = 'test', 
        email = 'test@mail.com',
        password = 'testpassword123',
        is_verified = True
    )
    return user

@pytest.fixture
def active_user_with_token(active_user):
    # creates token for this user in db
    token , created = Token.objects.get_or_create(user=active_user)
    return active_user, token.key

@pytest.fixture
def email_token(active_user):
    return create_token('user_email', active_user.email)

@pytest.fixture
def invalid_email_token(active_user):
    return create_token('user_email', 'test2@mail.com')

@pytest.fixture
def jwt_refresh_token(client, active_user):
    username_email, password = active_user.username, 'testpassword123'
    url = reverse('account:api-v1:jwt-create')
    data = {
        'username_email':username_email,
        'password':password
    }
    response = client.post(path=url, data=data)
    refresh_token = response.data.get('refresh')
    return refresh_token

@pytest.fixture
def jwt_access_token(client, active_user):
    username_email, password = active_user.username, 'testpassword123'
    url = reverse('account:api-v1:jwt-create')
    data = {
        'username_email':username_email,
        'password':password
    }
    response = client.post(path=url, data=data)
    access_token = response.data.get('access')
    return access_token