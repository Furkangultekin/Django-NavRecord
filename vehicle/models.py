from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    vehicle_id = models.PositiveIntegerField(primary_key=True)
    vehicle_plate = models.CharField(max_length=10, null=False)


class NavRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='nav_record', on_delete=models.CASCADE)
    datetime = models.DateTimeField(editable=False)
    latitude = models.DecimalField(max_digits=7, decimal_places=2)
    longitude = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        # Automatic save for datetime
        self.datetime = timezone.now()
        return super(NavRecord, self).save(*args, **kwargs)
