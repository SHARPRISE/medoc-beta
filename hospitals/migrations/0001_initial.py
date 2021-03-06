# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('quartier', models.CharField(max_length=75)),
                ('adresse', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number1', models.CharField(max_length=16)),
                ('phone_number2', models.CharField(max_length=16)),
                ('specialite', models.CharField(max_length=50)),
            ],
        ),
    ]
