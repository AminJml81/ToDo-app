import pytest

from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from rest_framework.test import APIClient

from todo.models import Task

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user1():
    return User.objects.create_user(
        username = 'testuser1',
        email = 'test1@mail.com',
        password = 'testpass1'
    )

@pytest.fixture
def user2():
    return User.objects.create_user(
        username = 'testuser2',
        email='test2@mail.com',
        password = 'testpass1',
    )

@pytest.fixture
def user1_with_tasks(user1):
    tasks = ['first task for user1', 'duplication test', 'edit test', 'delete test']

    for task in tasks:
        Task.objects.create(
            user = user1,
            title = task,
            slug = slugify(task)
        )
    return user1

@pytest.fixture
def user2_with_tasks(user2):
    tasks = ['first task for user2', 'duplication test', 'edit_test', 'delete test', 'one more']

    for task in tasks:
        Task.objects.create(
            user = user2,
            title = task,
            slug = slugify(task)
        )
    
    return user2