# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0005_cds")]

    operations = [
        migrations.AlterField(
            model_name="colline",
            name="code",
            field=models.CharField(max_length=6, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="commune",
            name="code",
            field=models.CharField(max_length=6, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="district",
            name="code",
            field=models.CharField(unique=True, max_length=4),
        ),
        migrations.AlterField(
            model_name="province",
            name="code",
            field=models.CharField(max_length=6, unique=True, null=True, blank=True),
        ),
    ]
