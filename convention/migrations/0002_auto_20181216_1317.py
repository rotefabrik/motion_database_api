# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-16 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='label',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('year', 'slot')]),
        ),
    ]