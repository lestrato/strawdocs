# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-16 04:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_auto_20170316_0015'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([]),
        ),
    ]
