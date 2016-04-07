# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='active_date_start',
            field=models.DateField(default=datetime.date(2016, 4, 5), verbose_name=b'Date to start displayig page.'),
        ),
    ]
