# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0011_auto_20161017_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='code',
            field=models.CharField(unique=True, max_length=9),
        ),
    ]
