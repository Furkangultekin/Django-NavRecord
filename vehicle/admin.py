from django.contrib import admin
from . import models

# Register your models here.
class NavRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'datetime', 'latitude', 'longitude')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_id', 'vehicle_plate')


admin.site.register(models.NavRecord, NavRecordAdmin)
admin.site.register(models.Vehicle, VehicleAdmin)