# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0012_auto_20170319_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
