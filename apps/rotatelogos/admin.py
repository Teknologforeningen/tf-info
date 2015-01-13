from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from apps.rotatelogos.models import Logo

class LogoAdmin(OrderedModelAdmin):
    pass

admin.site.register(Logo, LogoAdmin)
