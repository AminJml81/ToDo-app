from django.urls import reverse

import pytest


# NOTE: user means authenticated user.
@pytest.mark.django_db
def test_user_get_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    user_tasks = user.tasks.all()
    for task in user_tasks:
        url = reverse("todo:api-v3:task-detail", kwargs={"slug": task.slug})
        response = client.get(path=url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_get_task(client, user1):
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "first-task-for-user1"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_user_get_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_user_get_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
