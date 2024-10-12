from django.urls import reverse

import pytest

from todo.models import Task


# NOTE: user means authenticated user.
@pytest.mark.django_db
def test_user_delete_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    task = Task.objects.get(title="delete test")
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "delete-test"})
    response = client.delete(path=url)
    assert response.status_code == 204

    # checking DELETE method deletes the task instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all()) + 1

    with pytest.raises(task.DoesNotExist):
        task.refresh_from_db()


@pytest.mark.django_db
def test_user_delete_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "unavailable"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No Task matches the given query."

    # checking DELETE method does not delete any tasks.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_delete_task(client, user1_with_tasks):
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "delete-test"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_delete_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v3:task-detail", kwargs={"slug": "unavailable"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
