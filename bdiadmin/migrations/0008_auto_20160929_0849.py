# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0007_auto_20160929_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='status',
            field=models.CharField(blank=True, max_length=5, null=True, help_text='Either Public, Conf, Ass, Prive  or Hospital status.', choices=[('Pub', 'Public'), ('Con', 'Conf'), ('Priv', 'Prive'), ('Ass', 'Ass'), ('HPub', 'HPublic'), ('HCon', 'HConf'), ('HPrv', 'HPrive')]),
        ),
    ]
