from django.urls import reverse

import pytest

from ....models import User

@pytest.mark.django_db
def test_register_user_with_valid_data(client):
    data = {
        'username' : 'test',
        'email': 'test@test.com',
        'password' : 'testpassword123',
        'password2': 'testpassword123'
    }
    url = reverse('account:api-v1:registration')
    response = client.post(path=url, data=data)
    response_data = response.data.get('detail')
    assert response.status_code == 201
    assert response_data == f"an activation email has been sent to {data['email']}"
    users = User.objects.all()
    assert len(users) == 1


@pytest.mark.django_db
@pytest.mark.parametrize('username, email, password, password2',[
    ('test', 'test2@mail.com', 'testpassword123', 'testpassword123'), # duplicate username
    ('test2', 'test@mail.com', 'testpassword123', 'testpassword123'), # duplicate email
    ('test2', 'test2@mail.com', 'testpassword123', 'testpassword321'), # password dont match
    ('test2', 'test2@mail.com', 'test', 'test'), # weakpassword
    ('test2', 'test2@mail.com', '123', '123'), # weakpassword
    ('test2', 'test2@mail.com', 'testtest', 'testtest'), #weakpassword
])
def test_register_user_with_invalid_data(client, user, username, email, password, password2):
    data = {
        'username': username, 
        'email': email,
        'password': password,
        'password2': password2,
    }

    url = reverse('account:api-v1:registration')
    response = client.post(path=url, data=data)
    assert response.status_code == 400
    users = User.objects.all()
    assert len(users) == 1