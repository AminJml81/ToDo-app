from django.urls import reverse
from django.template.defaultfilters import slugify

import pytest

from todo.models import Task


# NOTE: user means authenticated user.


def create_task_data(title, description, status):
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if status:
        data["status"] = status

    return data


STATUS_DICT = {"TD": "Todo", "IP": "InProgress", "DO": "Done"}


# NOTE POST: CREATE TASK.
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
    url = reverse("todo:api-v1:task-list-create")
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
    url = reverse("todo:api-v1:task-list-create")
    data = {"description": "bad data"}
    response = client.post(path=url, data=data)
    response_data = response.data.get("title")[0]
    assert response.status_code == 400
    assert response_data == "This field is required."

    # checking if new task was created or not.
    assert number_of_tasks_for_this_user == len(user1.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_create_task(client, user1):
    url = reverse("todo:api-v1:task-list-create")
    data = {"title": "first task for user1"}
    response = client.post(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
    # checking if new task was created or not.
    assert Task.objects.filter(user=user1).exists() == False


@pytest.mark.django_db
def test_user_create_task_with_duplicate_title(client, user1_with_tasks):
    user = user1_with_tasks
    # before post method
    number_of_tasks_for_this_user = len(user.tasks.all())
    client.force_authenticate(user)
    url = reverse("todo:api-v1:task-list-create")
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
    url = reverse("todo:api-v1:task-list-create")
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
    assert response_data["description"] == None
    assert response_data["status"] == "Todo"
    assert response_data["user"]["email"] == user1.email


# NOTE GET: List TASKS.
@pytest.mark.django_db
def test_user_list_tasks(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    url = reverse("todo:api-v1:task-list-create")
    response = client.get(path=url)
    tasks = response.data
    assert response.status_code == 200
    assert len(user.tasks.all()) == len(tasks)

    # checking if fetched tasks belongs to the current user.
    for task in tasks:
        assert task["user"]["email"] == user.email


@pytest.mark.django_db
def test_unauthenticated_user_list_tasks(client, user1):
    url = reverse("todo:api-v1:task-list-create")
    data = {"title": "first task for user1"}
    response = client.get(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


# NOTE GET: RETRIVE INSTANCE.
@pytest.mark.django_db
def test_user_get_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    user_tasks = user.tasks.all()
    for task in user_tasks:
        url = reverse("todo:api-v1:task-detail", kwargs={"slug": task.slug})
        response = client.get(path=url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_get_task(client, user1):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "first-task-for-user1"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_user_get_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_user_get_unavailable_task(client, user1_with_tasks):
    user = user1_with_tasks
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "not-available"})
    response = client.get(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


# NOTE PATCH: UPDATE TASK PARTIALLY.
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    task = Task.objects.get(title="edit test")
    number_of_tasks_for_this_user = len(user.tasks.all())
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_partially_with_no_data(client, user1):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_partially_with_valid_data_but_duplicate_title(
    client, user1_with_tasks
):
    user = user1_with_tasks
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No Task matches the given query."

    # checking PUT method does not create new instance.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_valid_data(client, user1_with_tasks):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_no_data(client, user1):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_task_with_valid_data_but_duplicate_title(
    client, user1_with_tasks
):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "edit-test"})
    data = {"description": "edited description for user1"}
    response = client.put(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_update_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
    data = {"title": "not available"}
    response = client.patch(path=url, data=data)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


# NOTE: DELETE TASK
@pytest.mark.django_db
def test_user_delete_task(client, user1_with_tasks):
    user = user1_with_tasks
    client.force_authenticate(user)
    number_of_tasks_for_this_user = len(user.tasks.all())
    task = Task.objects.get(title="delete test")
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "delete-test"})
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
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 404
    assert response_data == "No Task matches the given query."

    # checking DELETE method does not delete any tasks.
    assert number_of_tasks_for_this_user == len(user.tasks.all())


@pytest.mark.django_db
def test_unauthenticated_user_delete_task(client, user1_with_tasks):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "delete-test"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_unauthenticated_user_delete_unavailable_task(client, user1_with_tasks):
    url = reverse("todo:api-v1:task-detail", kwargs={"slug": "unavailable"})
    response = client.delete(path=url)
    response_data = response.data.get("detail")
    assert response.status_code == 401
    assert response_data == "Authentication credentials were not provided."
