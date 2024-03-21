from django.contrib import admin

# Register your models here.
from .models import CustomUser

from .models import Report

admin.site.register(CustomUser)

class AnonReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'report_text', 'attached file', 'report_status', 'report_number')
admin.site.register(Report)