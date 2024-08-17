# Generated by Django 4.2.15 on 2024-08-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=125)),
                ("description", models.TextField(max_length=500)),
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("DO", "Done"), ("TD", "Todo"), ("IP", "InProgress")],
                        default="TD",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_date",),
            },
        ),
    ]
