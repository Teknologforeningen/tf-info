from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel
from datetime import date, time, datetime, timedelta
from django.utils import timezone
import re

class Page(OrderedModel):
    url         = models.CharField("Url of page to display (relative to root).", max_length=90)
    duration    = models.PositiveIntegerField("Duration (seconds)", default=10)

    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    edited_by   = models.ForeignKey(User, blank=True, null=True)

    pause_at = models.DateTimeField(blank=True, null=True)

    active_time_start   = models.TimeField("Time of day to start displaying page.", default=time(0,0))
    active_time_end     = models.TimeField("Time of day to stop displaying page. ", default=time(0,0))
    active_date_start   = models.DateField("Date to start displayig page.", default=date.today())
    active_date_end     = models.DateField("Last date to display page.", blank=True, null=True)

    monday      = models.BooleanField(default=True)
    tuesday     = models.BooleanField(default=True)
    wednesday   = models.BooleanField(default=True)
    thursday    = models.BooleanField(default=True)
    friday      = models.BooleanField(default=True)
    saturday    = models.BooleanField(default=True)
    sunday      = models.BooleanField(default=True)

    # Returns True or False whether page should be displayed
    # Checks time, date and day of week.
    def is_active(self, current_time=timezone.now()):
            # import pdb; pdb.set_trace()
            # Check time of day
            now = current_time.time()
            if self.active_time_end > self.active_time_start:
                if now < self.active_time_start or now > self.active_time_end:
                    return False
            elif self.active_time_end < self.active_time_start:
                if now < self.active_time_start and now > self.active_time_end:
                    return False

            # Check date
            today = current_time.date()
            if today < self.active_date_start or (self.active_date_end is not None and today > self.active_date_end):
                return False

            # Check day of week
            week = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]
            weekday = current_time.weekday()
            if not week[weekday]:
                return False

            # Check if paused
            if self.is_paused(current_time):
                return False

            return True

    def is_paused(self, current_time=timezone.now()):
        # Check paused state
        if self.pause_at is None:
            return False

        # Paused more than 24h ago
        if current_time > self.pause_at + timedelta(hours=24):
            self.pause_at = None
            return False

        # Pause not active yet
        if current_time < self.pause_at:
            return False

        # Paused before today and time is now past 06:00
        if self.pause_at.date() < current_time.date() and current_time.time() > time(6,00):
            self.pause_at = None
            return False

        return True


    def save(self, *args, **kwargs):
        # Add root if not present
        if re.match(r'/', self.url) is None:
            self.url = '/%s'%self.url

        super(Page, self).save(*args, **kwargs)


