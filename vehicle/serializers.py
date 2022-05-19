from rest_framework import serializers
from .models import Vehicle, NavRecord


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'vehicle_plate']

    # Create a new vehicle
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    
class NavigationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavRecord
        fields = ['vehicle', 'datetime', 'latitude', 'longitude']

    # Create a new Navigation Record
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
