# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-28 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170128_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
    ]
