from django.urls import path, include
from .views import AddVehicleView, UpdateVehicleView, AddNavRecordView, LastPointsView, GetVehicleView, GetNavRecordView

urlpatterns = [
    path('add_vehicle', AddVehicleView.as_view()),  # adding an item url; /add
    path('get_vehicle', GetVehicleView.as_view()),
    path('update_vehicle', UpdateVehicleView.as_view()),
    path('add_nav_record', AddNavRecordView.as_view()),
    path('get_nav_record', GetNavRecordView.as_view()),
    path('last_nav_record', LastPointsView.as_view())
]