from django.urls import reverse
from django.template.defaultfilters import slugify

import pytest

from todo.models import Task
from .utils import create_task_data


# NOTE: user means authenticated user.
@pytest.mark.parametrize(
    "title, description, status",
    [
        ("just title", None, None),  # just title
        (None, "just description", None),  # just decription
        (None, None, "DO"),  # just status
        ("just title", "just description", None),  # title with description
        ("just title", None, "DO"),  # title with status
        (None, "just description", "DO"),  # description with status
        ("just title", "just description", "DO"),  # all of them
    ],
)
@pytest.mark.django_db
def test_user_update_task_partially_with_valid_data(
    client, user1_with_tasks, title, description, status
):
    user = user1_with_tasks
    client.force_authenticate(user)
    task = Task.objects.get(title="edit test")
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = create_task_data(title, description, status)
    response = client.patch(path=url, data=data)
    response_data = response.data
    assert response.status_code == 200
    task.refresh_from_db()

    # checking instance data
    #      from database    vs data recieved after patch.
    assert task.description == response_data["description"]
    assert task.title == response_data["title"]
    assert task.get_status_display() == response_data["status"]

    # checking new slug if title was changed.
    if title:
        assert task.slug == slugify(title)
    # checking if patch does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_update_task_partially_with_no_data(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    task = Task.objects.get(title="edit test")
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    response = client.patch(path=url)
    response_data = response.data
    assert response.status_code == 200
    task.refresh_from_db()

    # checking instance data
    #      from database    vs  data recieved after patch.
    assert task.description == response_data["description"]
    assert task.title == response_data["title"]
    assert task.get_status_display() == response_data["status"]

    # checking PATCH method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_update_task_partially_with_valid_data_but_duplicate_title(
    client, user1_with_tasks
):
    # this test checks that if new title for this user is duplicate
    # it should not allow.
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"title": "duplication test"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("non_field_errors")[0]
    assert response.status_code == 400
    assert response_data == "The fields user, title must make a unique set."

    # checking PATCH method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_partially_update_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No Task matches the given query."
    # checking PATCH method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_update_task_partially_with_valid_data(
    client, user1_with_tasks
):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_partially_with_no_data(client, user1):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_partially_with_valid_data_but_duplicate_title(
    client, user1_with_tasks
):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_partially_update_unavailable_task(
    client, user1_with_tasks
):
    user = user1_with_tasks
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."

    # checking PATCH method creates new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


# NOTE PUT UPDATE TASK
@pytest.mark.parametrize(
    "title, description, status",
    [
        ("just title", None, None),  # title
        ("just title", "just description", None),  # title with description
        ("just title", None, "DO"),  # title with status
        ("just title", "just description", "DO"),  # all of them
    ],
)
@pytest.mark.django_db
def test_user_update_task_with_valid_data(
    client, user1_with_tasks, title, description, status
):
    user = user1_with_tasks
    client.force_authenticate(user)
    task = Task.objects.get(title="edit test")
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = create_task_data(title, description, status)
    response = client.put(path=url, data=data)
    response_data = response.data
    assert response.status_code == 200
    task.refresh_from_db()

    # checking instance data
    #      from database    vs data recieved after patch.
    assert task.description == response_data["description"]
    assert task.title == response_data["title"]
    assert task.get_status_display() == response_data["status"]

    # checking new slug was changed.
    assert task.slug == slugify(title)
    # checking PUT does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_update_task_with_no_data(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    task = Task.objects.get(title="edit test")
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    response = client.put(path=url)
    response_data = response.data.get("title")[0]
    assert response.status_code == 400
    assert response_data == "This field is required."
    task.refresh_from_db()

    # checking PUT method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_update_task_with_valid_data_but_duplicate_title(client, user1_with_tasks):
    # this test checks that if new title for this user is duplicate
    # it should not allow.
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"title": "duplication test"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("non_field_errors")[0]
    assert response.status_code == 400
    assert response_data == "The fields user, title must make a unique set."

    # checking PUT method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user_update_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No Task matches the given query."

    # checking PUT method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_valid_data(client, user1_with_tasks):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_no_data(client, user1):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_valid_data_but_duplicate_title(
    client, user1_with_tasks
):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v4:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
