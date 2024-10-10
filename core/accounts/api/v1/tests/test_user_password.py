from django.urls import reverse

from django.contrib.auth import authenticate

import pytest


@pytest.mark.django_db
def test_change_password_with_token_with_valid_data(client, active_user_with_token):
    url = reverse('account:api-v1:change-password')
    token = active_user_with_token[1]
    data = {
        'current_password': 'testpassword123',
        'new_password': 'testpassword321',
        'new_password2': 'testpassword321'
    }
    headers = {'Authorization': f'Token {token}'}
    response = client.put(path=url, data=data, headers=headers)
    response_data =  response.data.get('Message')
    assert response.status_code == 200
    assert response_data == 'your password was successfully changed.'

    # testing if password was changed or not using simple authenticate.
    user = authenticate(response.request, username='test', password='testpassword321')
    assert user is not None


@pytest.mark.django_db
def test_change_password_with_jwt_token_with_valid_data(client, jwt_access_token):
    url = reverse('account:api-v1:change-password')
    data = {
        'current_password': 'testpassword123',
        'new_password': 'testpassword321',
        'new_password2': 'testpassword321'
    }
    headers = {'Authorization': f'Bearer {jwt_access_token}'}
    response = client.put(path=url, data=data, headers=headers)
    response_data =  response.data.get('Message')
    assert response.status_code == 200
    assert response_data == 'your password was successfully changed.'

    # testing if password was changed or not using simple authenticate.
    user = authenticate(response.request, username='test', password='testpassword321')
    assert user is not None


@pytest.mark.parametrize('current_password, new_password, new_password2',[
    ('test', 'testpass123', 'testpass123'), # invalid current password
    ('testpassword123', 'testpass123', 'testpass321'), # new passwords dont match
    ('testpassword123', 'test1', 'test1'), # new passwords are weak
    ('testpassword123', '123', '123'), # new passwords are weak
])
@pytest.mark.django_db
def test_change_password_with_token_with_invalid_data(client, active_user_with_token, current_password, new_password, new_password2):
    url = reverse('account:api-v1:change-password')
    user, token = active_user_with_token[0], active_user_with_token[1]
    data = {
        'current_password': current_password,
        'new_password': new_password,
        'new_password2': new_password2
    }
    headers = {'Authorization': f'Token {token}'}
    response = client.put(path=url, data=data, headers=headers)
    assert response.status_code == 400


@pytest.mark.parametrize('current_password, new_password, new_password2',[
    ('test', 'testpass123', 'testpass123'), # invalid current password
    ('testpassword123', 'testpass123', 'testpass321'), # new passwords dont match
    ('testpassword123', 'test1', 'test1'), # new passwords are weak
    ('testpassword123', '123', '123'), # new passwords are weak
])
@pytest.mark.django_db
def test_change_password_with_jwt_token_with_invalid_data(client, jwt_access_token, current_password, new_password, new_password2):
    url = reverse('account:api-v1:change-password')
    data = {
        'current_password': current_password,
        'new_password': new_password,
        'new_password2': new_password2
    }
    headers = {'Authorization': f'Bearer {jwt_access_token}'}
    response = client.put(path=url, data=data, headers=headers)
    assert response.status_code == 400


@pytest.mark.django_db
def test_change_password_without_token(client, user):
    url = reverse('account:api-v1:change-password')
    data = {
        'current_password': 'testpassword123',
        'new_password': 'testpassword321',
        'new_password2': 'testpassword321'
    }
    response = client.put(path=url, data=data)
    response_data =  response.data.get('detail')
    assert response.status_code == 401
    assert response_data == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_reset_password_with_valid_data(client):
    url = reverse('account:api-v1:reset-password')
    data = {
        'email': 'test@mail.com',
    }
    response = client.post(path=url, data=data)
    response_data =  response.data.get('Message')
    assert response.status_code == 200
    assert response_data == f"we have sent an email to {data['email']}."


@pytest.mark.django_db
def test_reset_password_with_invalid_data(client):
    # given email field is not actually email.
    url = reverse('account:api-v1:reset-password')
    data = {
        'email': 'test',
    }
    response = client.post(path=url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_password_with_unregistered_email(client, user):
    # there is no user with this email.
    url = reverse('account:api-v1:reset-password')
    data = {
        'email': 'test123@mail.com',
    }
    response = client.post(path=url, data=data)
    response_data =  response.data.get('Message')
    assert response.status_code == 200
    assert response_data == f"we have sent an email to {data['email']}."


@pytest.mark.django_db
def test_reset_password_confirm_with_valid_token_with_valid_data(client, email_token):
    url = reverse('account:api-v1:reset-password-confirm', kwargs={'token':email_token})
    data = {
        'new_password': 'testpass321',
        'new_password2': 'testpass321'
    }
    response = client.put(path=url, data=data)
    response_data =  response.data.get('Message')
    assert response.status_code == 200
    assert response_data == "your password was successfully reset"

    # testing if password was changed or not using simple authenticate.
    user = authenticate(response.request, username='test@mail.com', password='testpass321')
    assert user is not None
    
    
@pytest.mark.django_db
def test_reset_password_confirm_with_invalid_token_with_valid_data(client):
    email_token = 'asdasd'
    url = reverse('account:api-v1:reset-password-confirm', kwargs={'token':email_token})
    data = {
        'new_password': 'testpass321',
        'new_password2': 'testpass321'
    }
    response = client.put(path=url, data=data)
    response_data =  response.data.get('Message')
    assert response.status_code == 400
    assert response_data == 'Token is invalid or expired'


@pytest.mark.parametrize('new_password, new_password2', [
    ('testpass321', 'testpass123'), # new passwords dont match
    ('test', 'test'), # new passwords are weak
    ('123', '123') # new passwords are weak
])
@pytest.mark.django_db
def test_reset_password_confirm_with_valid_token_with_invalid_data(client, email_token, new_password, new_password2):
    url = reverse('account:api-v1:reset-password-confirm', kwargs={'token':email_token})
    data = {
        'new_password': new_password,
        'new_password2': new_password2
    }
    response = client.put(path=url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_password_confirm_with_invalid_token(client, invalid_email_token):
    # there is no user with this email.
    url = reverse('account:api-v1:reset-password-confirm', kwargs={'token':invalid_email_token})
    data = {
        'new_password': 'testtest123',
        'new_password2': 'testtest123'
    }
    response = client.put(path=url, data=data)
    response_data =  response.data.get('detail')
    assert response.status_code == 404
    assert response_data == 'No User matches the given query.'