# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-16 12:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('convention', '0001_initial'),
        ('submitter', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=512)),
                ('body', models.TextField()),
                ('pdf_name', models.CharField(max_length=512)),
                ('status', models.CharField(choices=[('not_voted', 'nicht abgestimmt'), ('dismissed', 'erledigt'), ('referred', '\xfcberwiesen'), ('accepted', 'angenommen'), ('rejected', 'abgelehnt')], max_length=64)),
                ('added', models.DateTimeField()),
                ('convention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convention.Convention')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='motion',
            name='referrals',
            field=models.ManyToManyField(to='motion.Referral'),
        ),
        migrations.AddField(
            model_name='motion',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convention.Section'),
        ),
        migrations.AddField(
            model_name='motion',
            name='submitters',
            field=models.ManyToManyField(to='submitter.Submitter'),
        ),
    ]
