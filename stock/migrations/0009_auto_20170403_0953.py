# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-03 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stock", "0008_auto_20170330_0813")]

    operations = [
        migrations.RenameField(
            model_name="stockoutreport", old_name="produit", new_name="product"
        ),
        migrations.AlterField(
            model_name="report",
            name="category",
            field=models.CharField(
                choices=[
                    (b"REG", "Registering"),
                    (b"SF", "Final Stock"),
                    (b"SR", "Stoc Received"),
                    (b"RP", "Rupture"),
                ],
                max_length=3,
            ),
        ),
    ]
