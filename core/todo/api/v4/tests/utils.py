STATUS_DICT = {"TD": "Todo", "IP": "InProgress", "DO": "Done"}


def create_task_data(title, description, status):
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if status:
        data["status"] = status

    return data
