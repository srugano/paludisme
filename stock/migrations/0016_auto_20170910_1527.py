# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-10 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stock", "0015_casespaluprov")]

    operations = [
        migrations.AddField(
            model_name="casespaluprov", name="ge", field=models.FloatField(default=0.0)
        ),
        migrations.AddField(
            model_name="casespaluprov", name="tdr", field=models.FloatField(default=0.0)
        ),
    ]
