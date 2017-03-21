# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0009_profileuser_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='level',
            field=models.CharField(default='', help_text='The facility attached to this user.', max_length=16, blank=True),
        ),
    ]
