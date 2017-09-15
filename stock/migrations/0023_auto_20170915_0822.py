# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 08:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0022_auto_20170912_0428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casespalucds',
            name='cds',
        ),
        migrations.RemoveField(
            model_name='casespaludis',
            name='district',
        ),
        migrations.RemoveField(
            model_name='casespaluprov',
            name='province',
        ),
        migrations.RemoveField(
            model_name='stockproductcds',
            name='cds',
        ),
        migrations.RemoveField(
            model_name='stockproductdis',
            name='district',
        ),
        migrations.RemoveField(
            model_name='stockproductprov',
            name='province',
        ),
        migrations.DeleteModel(
            name='CasesPaluCDS',
        ),
        migrations.DeleteModel(
            name='CasesPaluDis',
        ),
        migrations.DeleteModel(
            name='CasesPaluProv',
        ),
        migrations.DeleteModel(
            name='StockProductCDS',
        ),
        migrations.DeleteModel(
            name='StockProductDis',
        ),
        migrations.DeleteModel(
            name='StockProductProv',
        ),
    ]
