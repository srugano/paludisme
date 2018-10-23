# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-10 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bdiadmin", "0013_auto_20170319_1415"),
        ("stock", "0019_stockproductprov"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockProductCDS",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.PositiveIntegerField(default=2017)),
                ("week", models.CharField(max_length=3)),
                ("product", models.CharField(max_length=50)),
                ("quantity", models.FloatField(default=0.0)),
                (
                    "cds",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bdiadmin.CDS"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockProductDis",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.PositiveIntegerField(default=2017)),
                ("week", models.CharField(max_length=3)),
                ("product", models.CharField(max_length=50)),
                ("quantity", models.FloatField(default=0.0)),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bdiadmin.District",
                    ),
                ),
            ],
        ),
    ]
