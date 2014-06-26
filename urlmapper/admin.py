from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import URLMap

import settings


class URLMapAdmin(admin.ModelAdmin):

    list_display = ('key', 'mapping_type', 'get_url')

    fieldsets = [(None, {'fields': ('key',)})]
    if 'url' in settings.URLMAPPER_ALLOWED_MAPPINGS:
        fieldsets.append((_("URL mapping"), {'fields': ('url',)}))
    if 'object' in settings.URLMAPPER_ALLOWED_MAPPINGS:
        fieldsets.append((_("Object mapping"), {'fields': ('content_type', 'object_id')}))
    if 'view_name' in settings.URLMAPPER_ALLOWED_MAPPINGS:
        fieldsets.append((_("View mapping"), {'fields': ('view_name', 'view_keywords')}))


admin.site.register(URLMap, URLMapAdmin)
