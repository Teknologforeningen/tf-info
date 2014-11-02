from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from manager.models import Page
from django.utils import timezone

class PageAdmin(OrderedModelAdmin):

    list_display = ('title', 'is_paused', 'move_up_down_links')

    fieldsets = (
        (None, {'fields': ('url', 'duration', 'title', 'description', 'creator', 'paused_at')}),
        ('Date and Time', {'fields': ('active_time_start', 'active_time_end', 'active_date_start', 'active_date_end')}),
        ('Weekdays', {'fields': (('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'),)})
    )

    actions = ['pause', 'unpause']

    def pause(self, request, queryset):
        queryset.update(paused_at=timezone.now())

    def unpause(self, request, queryset):
        queryset.update(paused_at=None)

    def save_model(self, request, obj, form, change):
        if obj.creator is None:
            obj.creator = request.user
        obj.save()

admin.site.register(Page, PageAdmin)