# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20160405_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='active_date_start',
            field=models.DateField(default=datetime.date(2017, 4, 10), verbose_name=b'Date to start displaying page.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.ImageField(upload_to=b'images/', null=True, verbose_name=b'Image to show instead of URL. If image is specified URL wont be used', blank=True),
        ),
    ]
