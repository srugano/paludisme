# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0010_auto_20161017_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='level',
            field=models.CharField(default='', help_text='The facility attached to this user.', max_length=7, blank=True),
        ),
    ]
