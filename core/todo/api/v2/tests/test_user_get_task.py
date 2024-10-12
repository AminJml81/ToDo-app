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


@pytest.mark.django_db
def test_user_get_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    user_tasks = user.tasks.all()
    for task in user_tasks:
        url = reverse("todo:api-v2:task-detail", kwargs={"slug": task.slug})
        response = client.get(path=url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_get_task(client, user1):
    url = reverse("todo:api-v2:task-detail", kwargs={"slug": "first-task-for-user1"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_user_get_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    url = reverse("todo:api-v2:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_user_get_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v2:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
