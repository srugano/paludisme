# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-21 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("stock", "0012_auto_20170720_1148")]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bdiadmin.CDS",
            ),
        ),
        migrations.AlterField(
            model_name="reporter",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bdiadmin.CDS",
            ),
        ),
    ]
