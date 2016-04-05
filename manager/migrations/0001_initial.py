# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('url', models.CharField(max_length=90, verbose_name=b'Url of page to display (relative to root).')),
                ('duration', models.PositiveIntegerField(default=10, verbose_name=b'Duration (seconds)')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('pause_at', models.DateTimeField(null=True, blank=True)),
                ('hide_top_bar', models.BooleanField(default=False, verbose_name=b'Hide the top bar of the screen')),
                ('hide_bottom_bar', models.BooleanField(default=False, verbose_name=b'Hide the bottom bar of the screen')),
                ('active_time_start', models.TimeField(default=datetime.time(0, 0), verbose_name=b'Time of day to start displaying page.')),
                ('active_time_end', models.TimeField(default=datetime.time(0, 0), verbose_name=b'Time of day to stop displaying page. ')),
                ('active_date_start', models.DateField(default=datetime.date(2016, 4, 4), verbose_name=b'Date to start displayig page.')),
                ('active_date_end', models.DateField(null=True, verbose_name=b'Last date to display page.', blank=True)),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wednesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=True)),
                ('sunday', models.BooleanField(default=True)),
                ('edited_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
