# Generated by Django 4.1.1 on 2022-10-24 13:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Hello_Buddy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="image_upload",
            field=models.ImageField(blank=True, null=True, upload_to="event/images"),
        ),
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateTimeField(verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(max_length=20, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="event",
            name="participant",
            field=models.PositiveIntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Participant",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="place",
            field=models.CharField(max_length=50, verbose_name="Place"),
        ),
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.CharField(max_length=20, null=True, verbose_name="Type"),
        ),
    ]
