# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-25 00:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('blog', '0013_remove_blogindexpage_intro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogtagindexpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='BlogTagIndexPage',
        ),
    ]
