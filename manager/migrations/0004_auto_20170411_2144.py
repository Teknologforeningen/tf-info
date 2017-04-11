# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20170410_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='active_date_start',
            field=models.DateField(default=datetime.date(2017, 4, 11), verbose_name=b'Date to start displaying page.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(max_length=1024, verbose_name=b'Url of page to display (relative to root).'),
        ),
    ]
