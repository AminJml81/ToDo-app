from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from faker import Faker

import random

from todo.models import Task
from accounts.models import User


class Command(BaseCommand):
    help = "Creates some tasks for a user"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", nargs="?", type=int, default=5, help="number of tasks to create."
        )

    def handle(self, *args, **options):
        task_number = options["n"]
        self.user = self.create_user()
        for _ in range(task_number):
            title = self.fake.text(max_nb_chars=20)
            Task.objects.create(
                user=self.user,
                title=title,
                slug=slugify(title),
                description=self.fake.paragraph(nb_sentences=2),
                status=random.choice(Task.TaskStatus.choices)[0],
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Created "%i" Tasks for "%s".'
                % (task_number, self.user.email)
            )
        )

    def create_user(self):
        email = self.fake.email()
        user = User.objects.create_user(
            email=email, password=self.fake.password(), username=email.split("@")[0]
        )
        return user
