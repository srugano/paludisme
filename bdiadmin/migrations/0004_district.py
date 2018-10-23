# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0003_auto_20160321_1133")]

    operations = [
        migrations.CreateModel(
            name="District",
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
                    models.CharField(unique=True, max_length=40, verbose_name="nom"),
                ),
                ("code", models.IntegerField(unique=True)),
                (
                    "province",
                    models.ForeignKey(verbose_name=b"province", to="bdiadmin.Province"),
                ),
            ],
            options={"ordering": ("name",)},
        )
    ]
