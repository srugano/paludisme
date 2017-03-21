# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colline',
            name='code',
            field=models.IntegerField(unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='colline',
            name='name',
            field=models.CharField(max_length=30, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='code',
            field=models.IntegerField(unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='province',
            name='code',
            field=models.IntegerField(unique=True, null=True, blank=True),
        ),
    ]
