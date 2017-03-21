# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0008_auto_20160929_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='level',
            field=models.TextField(default='', blank=True),
        ),
    ]
