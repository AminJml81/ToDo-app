from django.urls import reverse
from django.template.defaultfilters import slugify

import pytest

from todo.models import Task
from .utils import create_task_data, STATUS_DICT


# NOTE: user means authenticated user.
@pytest.mark.parametrize(
    "title, description, status",
    [
        ("title", None, None),  # just title
        ("title", "description", None),  # title with description
        ("title", None, "IP"),  # title with status
        ("title", "description", "DO"),  # all of them
    ],
)
@pytest.mark.django_db
def test_user_create_task_with_valid_data(client, user1, title, description, status):
    client.force_authenticate(user1)
    number_of_tasks_for_this_user = len(user1.tasks.all())
    url = reverse("todo:api-v2:task-list-create")
    data = create_task_data(title, description, status)
    response = client.post(path=url, data=data)
    response_data = response.data
    assert response.status_code == 201

    task = Task.objects.get(title=title)
    # checking new task fields.
    assert response_data["title"] == task.title == title
    assert response_data["description"] == task.description == description
    assert (
        response_data["status"]
        == task.get_status_display()
        == (STATUS_DICT[status] if status is not None else "Todo")
    )
    assert response_data["user"]["email"] == task.user.email

    # checking task slug.
    assert task.slug == slugify(title)

    # checking if new task was created or not.
    assert number_of_tasks_for_this_user + 1 == len(user1.tasks.all())


@pytest.mark.django_db
def test_user_create_task_with_invalid_data(client, user1):
    # if title is not given then the given data is invalid
    client.force_authenticate(user1)
    number_of_tasks_for_this_user = len(user1.tasks.all())
    url = reverse("todo:api-v2:task-list-create")
    data = {"description": "bad data"}
    response = client.post(path=url, data=data)
    response_data = response.data.get("title")[0]
    assert response.status_code == 400
    assert response_data == "This field is required."

    # checking if new task was created or not.
    assert number_of_tasks_for_this_user == len(user1.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_create_task(client, user1):
    url = reverse("todo:api-v2:task-list-create")
    data = {"title": "first task for user1"}
    response = client.post(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
    # checking if new task was created or not.
    assert not Task.objects.filter(user=user1).exists()


@pytest.mark.django_db
def test_user_create_task_with_duplicate_title(client, user1_with_tasks):
    user = user1_with_tasks
    # before post method
    number_of_tasks_for_this_user = len(user.tasks.all())
    client.force_authenticate(user)
    url = reverse("todo:api-v2:task-list-create")
    data = {"title": "first task for user1"}
    response = client.post(path=url, data=data)
    response_data = response.data.get("non_field_errors")[0]
    assert response.status_code == 400
    assert response_data == "The fields user, title must make a unique set."

    # after post method
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_user2_create_task_with_exact_title_that_user1_has_task(
    client, user2_with_tasks, user1
):
    # user1 should create this new task successfully.
    # before post method
    number_of_tasks_for_this_user = len(user1.tasks.all())
    client.force_authenticate(user1)
    url = reverse("todo:api-v2:task-list-create")
    data = {
        # user2 has taks with exactly this title
        "title": "duplication test"
    }
    response = client.post(path=url, data=data)
    response_data = response.data
    assert response.status_code == 201

    # assert one task for this user has been created.
    assert number_of_tasks_for_this_user + 1 == len(user1.tasks.all())

    # checking fields of new created task.
    assert response_data["title"] == "duplication test"
    assert response_data["description"] is None
    assert response_data["status"] == "Todo"
    assert response_data["user"]["email"] == user1.email
