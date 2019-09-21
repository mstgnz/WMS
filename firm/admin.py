from django.contrib import admin
from .models import Firm

class FirmAdmin(admin.ModelAdmin):
    list_display = ['name','full_name','create_date']
    list_display_links = ['name','full_name']
    list_filter = ['create_date']

    class Meta:
        model = Firm



admin.site.register(Firm, FirmAdmin)
