# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-25 02:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20170525_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='comments',
        ),
        migrations.DeleteModel(
            name='BlogComment',
        ),
    ]
