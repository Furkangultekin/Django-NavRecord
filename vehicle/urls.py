from django.urls import path, include
from .views import VehicleView, UpdateVehicleView, AddNavRecordView, LastPointsView

urlpatterns = [
    path('add_vehicle', VehicleView.as_view()),
    path('get_vehicle', VehicleView.as_view()),
    path('update_vehicle', UpdateVehicleView.as_view()),
    path('add_nav_record', AddNavRecordView.as_view()),
    path('get_nav_record', AddNavRecordView.as_view()),
    path('last_nav_record', LastPointsView.as_view())
]
