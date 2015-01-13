from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel
from datetime import date, time, datetime, timedelta
from django.utils import timezone
import re

class Logo(OrderedModel):
    url         = models.CharField("Url of page to display (relative to root).", max_length=90)
    duration    = models.PositiveIntegerField("Duration (seconds)", default=10)
