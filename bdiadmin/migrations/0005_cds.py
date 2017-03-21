# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0004_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='CDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(unique=True, max_length=6)),
                ('status', models.CharField(blank=True, max_length=4, null=True, help_text='Either Public, Conf, Ass, Prive  or Hospital status.', choices=[(b'Pub', b'Public'), (b'Con', b'Conf'), (b'Priv', b'Prive'), (b'Ass', b'Ass'), (b'HPub', b'HPublic'), (b'HCon', b'HConf'), (b'HPrv', b'HPrive')])),
                ('district', models.ForeignKey(to='bdiadmin.District')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
