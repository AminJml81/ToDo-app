from django.urls import reverse

from rest_framework.authtoken.models import Token

import pytest


@pytest.mark.django_db
def test_login_with_token_with_username_for_active_user_without_token_in_db(client, active_user):
    username_email, password = active_user.username, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_with_token_by_username_for_active_user_without_token_in_db(client, active_user):
    username_email, password = active_user.username, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_with_token_by_username_for_active_user_with_token_in_db(client, active_user_with_token):
    active_user = active_user_with_token[0]
    username_email, password = active_user.username, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_with_token_by_email_for_active_user_without_token_in_db(client, active_user):
    username_email, password = active_user.email, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_with_token_by_email_for_active_user_with_token_in_db(client, active_user_with_token):
    active_user = active_user_with_token[0]
    username_email, password = active_user.email, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_with_token_by_username_for_user_without_token_in_db(client, user):
    #NOTE: <user> is not verified.
    username_email, password = user.username, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    response_data = response.data.get('not verified')[0]
    assert response.status_code == 400
    assert response_data == 'User is not verified.'


@pytest.mark.django_db
def test_login_with_token_by_email_for_user_without_token_in_db(client, user):
    #NOTE: <user> is not verified.
    username_email, password = user.email, 'testpassword123'
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    response_data = response.data.get('not verified')[0]
    assert response.status_code == 400
    assert response_data == 'User is not verified.'


@pytest.mark.django_db
@pytest.mark.parametrize('username_email, password', [
    ('test', 'testpassword12'), # correct username ,wrong password.
    ('test2', 'testpassword123'), # no user with this username.
    ('test@mail.com', 'testpassword12'), # correct email, wrong password.
    ('testt@mail.com', 'testpassword123') # no user with this email.
])
def test_login_with_token_by_username_with_invalid_credentials(client, username_email, password):
    url = reverse('account:api-v1:token-login')
    data = {'username_email':username_email, 'password':password}
    response = client.post(path=url, data=data)
    response_data = response.data.get('credentials error')[0]
    assert response.status_code == 400
    assert response_data == 'Unable to log in with provided credentials.'


@pytest.mark.django_db
def test_authorized_user_token_logout(client, active_user_with_token):
    user, token = active_user_with_token[0], active_user_with_token[1]
    token_from_db = Token.objects.get(user=user.id)
    header = {'AUTHORIZATION': f'Token {token}'}
    url = reverse('account:api-v1:token-logout')
    response = client.get(path=url, headers=header)
    assert response.status_code == 204
    with pytest.raises(Token.DoesNotExist):
        token_from_db.refresh_from_db()


@pytest.mark.django_db
def test_unauthorized_user_token_logout(client):
    url = reverse('account:api-v1:token-logout')
    response = client.get(path=url)
    response_data = response.data.get('detail')
    assert response.status_code == 401
    assert response_data == 'Authentication credentials were not provided.'