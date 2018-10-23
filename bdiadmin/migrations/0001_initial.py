# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Colline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(unique=True, max_length=20, verbose_name="name"),
                ),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Commune",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(unique=True, max_length=20, verbose_name="name"),
                ),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="ProfileUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
                        blank=True,
                        help_text="The telephone to contact you.",
                        max_length=16,
                        verbose_name="telephone",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex=b"^\\+?1?\\d{9,15}$",
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                            )
                        ],
                    ),
                ),
                ("user", models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Province",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(unique=True, max_length=20, verbose_name="name"),
                ),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.AddField(
            model_name="commune",
            name="province",
            field=models.ForeignKey(to="bdiadmin.Province"),
        ),
        migrations.AddField(
            model_name="colline",
            name="commune",
            field=models.ForeignKey(to="bdiadmin.Commune"),
        ),
    ]
