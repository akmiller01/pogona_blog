# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-25 01:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20170525_0143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpagecomments',
            old_name='page',
            new_name='blog',
        ),
    ]
