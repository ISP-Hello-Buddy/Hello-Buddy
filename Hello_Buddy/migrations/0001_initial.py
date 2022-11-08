# Generated by Django 4.1.1 on 2022-11-08 08:44

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=20, verbose_name="Name")),
                ("place", models.CharField(max_length=50, verbose_name="Place")),
                (
                    "participant",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Participant",
                    ),
                ),
                (
                    "joined",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(
                                models.PositiveIntegerField(
                                    default=1,
                                    validators=[
                                        django.core.validators.MinValueValidator(1)
                                    ],
                                    verbose_name="Participant",
                                )
                            )
                        ],
                    ),
                ),
                ("date", models.DateField(verbose_name="Date")),
                (
                    "time",
                    models.TimeField(default=datetime.time(0, 0), verbose_name="Time"),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("eating", "Eating"),
                            ("sport", "Sport"),
                            ("movie", "Movie"),
                            ("party", "Party"),
                            ("education", "Education"),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name="Type",
                    ),
                ),
                (
                    "image_upload",
                    models.ImageField(
                        blank=True,
                        default="event/images/default.jpg",
                        null=True,
                        upload_to="event/images",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                (
                    "avatar",
                    models.ImageField(
                        default="default.jpg", upload_to="profile_images"
                    ),
                ),
                ("bio", models.TextField(default="...", max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParticipantOfEvent",
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
                (
                    "event",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Hello_Buddy.event",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HostOfEvent",
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
                (
                    "event",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Hello_Buddy.event",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
