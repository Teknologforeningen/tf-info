from django.test import TestCase
from manager.models import Page
from datetime import datetime, timedelta
from django.utils import timezone

class PageTestCase(TestCase):
    def setUp(self):
        now = timezone.now()
        Page.objects.create(url="testurl", description="test description")

    def test_regular_page_active(self):
        """Page with no pause or time/date range is active."""
        page = Page.objects.get(url="/testurl")

        self.assertFalse(page.is_paused())
        self.assertTrue(page.is_active())

    def test_paused_page_not_active(self):
        """Page that has been paused is not active."""
        page = Page.objects.get(url="/testurl")
        page.pause_at = timezone.now().replace(hour=12)
        current_time = timezone.now().replace(hour=13)

        self.assertTrue(page.is_paused(current_time))
        self.assertFalse(page.is_active(current_time))

    def test_previously_paused_page_active(self):
        """Page that has is not paused but has been in the past is active."""
        page = Page.objects.get(url="/testurl")
        page.paused_at = timezone.now() - timedelta(hours=48)

        self.assertFalse(page.is_paused())
        self.assertTrue(page.is_active())

        page.paused_at = timezone.now()
        morning = timezone.now().replace(hour=6)

        self.assertFalse(page.is_paused(morning))
        self.assertTrue(page.is_active(morning))

    def test_page_active_time_of_day(self):
        """Page has certain times of day it should be visible."""
        page = Page.objects.get(url="/testurl")
        now = timezone.now().replace(hour=12)

        # Default page has no times -> active
        self.assertTrue(page.is_active(now))

        # Set start time in the future
        page.active_time_start = now.replace(hour=13).time()
        self.assertTrue(page.active_time_start > now.time())
        self.assertFalse(page.is_active(now))

        # Set time to be past start time
        now = now.replace(hour=14)
        self.assertTrue(page.is_active(now))

        # Set end time in the future, still active
        page.active_time_end = now.replace(hour=15).time()
        self.assertTrue(page.is_active(now))

        # Set time to be past end-time -> inactive
        now = now.replace(hour=16)
        self.assertFalse(page.is_active(now))

        # Set start time in the future but bigger than end-time
        page.active_time_start = now.replace(hour=17).time()
        self.assertFalse(page.is_active(now))

        # Time bigger than start time in the evening
        now = now.replace(hour=19)
        self.assertTrue(page.is_active(now))

    def test_page_date_range(self):
        """Page has certains dates it should be visible."""
        page = Page.objects.get(url="/testurl")
        now = timezone.now()
        today = now.date()

        page.active_date_start = today
        self.assertTrue(page.is_active(now))

        page.active_date_start = today + timedelta(days=1)
        self.assertFalse(page.is_active(now))

        page.active_date_start = today - timedelta(days=7)
        page.active_date_end = today - timedelta(days=3)
        self.assertFalse(page.is_active(now))

    def test_page_weekdays(self):
        """Page is active on certain weekdays"""
        page = Page.objects.get(url="/testurl")
        now = timezone.make_aware(datetime(2014, 4, 28, 16, 53), timezone.get_current_timezone()) # Monday
        page.active_date_start = now.date()

        self.assertTrue(page.is_active(now))

        page.monday = False
        self.assertFalse(page.is_active(now))

        now = now + timedelta(days=1)
        self.assertTrue(page.is_active(now))

    def test_timezone(self):
        """Timezone should be Helsinki"""
        now = timezone.now()
        self.assertTrue(timezone.get_current_timezone_name() == 'Europe/Helsinki')

