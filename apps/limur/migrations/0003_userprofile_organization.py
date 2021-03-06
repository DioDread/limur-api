# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('limur', '0002_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='organization',
            field=models.ForeignKey(blank=True, help_text='Organization associated with user', null=True, on_delete=django.db.models.deletion.CASCADE, to='limur.Organization'),
        ),
    ]
