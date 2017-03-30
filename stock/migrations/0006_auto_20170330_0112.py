# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-30 01:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0013_auto_20170319_1415'),
        ('stock', '0005_dosage_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')], verbose_name='telephone')),
                ('supervisor_phone_number', models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')], verbose_name='telephone')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdiadmin.CDS')),
            ],
        ),
        migrations.AlterField(
            model_name='reporter',
            name='phone_number',
            field=models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')], verbose_name='telephone'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='supervisor_phone_number',
            field=models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')], verbose_name='telephone'),
        ),
    ]
