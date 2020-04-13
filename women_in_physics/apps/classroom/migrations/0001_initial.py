# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-13 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name=b'Class Name')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=40)),
                ('answer', models.TextField(max_length=10000)),
                ('hidden', models.BooleanField(default=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name=b'Username')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name=b'Username')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='classroom.Student'),
        ),
        migrations.AddField(
            model_name='classes',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='classroom.Teacher'),
        ),
    ]
