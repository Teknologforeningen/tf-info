from django.contrib import admin
from apps.rotatelogos.models import Logo

class LogoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Logo, LogoAdmin)
