# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-22 20:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20170521_0145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='intro',
        ),
    ]
