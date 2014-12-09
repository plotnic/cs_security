# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=128)),
                ('app', models.CharField(max_length=128)),
                ('key', models.CharField(max_length=256)),
            ],
            options=None,
            bases=None,
        ),
    ]
