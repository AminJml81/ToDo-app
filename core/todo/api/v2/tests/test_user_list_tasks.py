from django.urls import reverse

import pytest


# NOTE: user means authenticated user.
@pytest.mark.django_db
def test_user_list_tasks(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    url = reverse("todo:api-v2:task-list-create")
    response = client.get(path=url)
    tasks = response.data
    assert response.status_code == 200
    assert len(user.tasks.all()) == len(tasks)

    # checking if fetched tasks belongs to the current user.
    for task in tasks:
        assert task["user"]["email"] == user.email


@pytest.mark.django_db
def test_unauthenticated_user_list_tasks(client, user1):
    url = reverse("todo:api-v2:task-list-create")
    data = {"title": "first task for user1"}
    response = client.get(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
