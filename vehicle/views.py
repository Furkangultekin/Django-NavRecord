from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import VehicleSerializer, NavigationRecordSerializer
from .models import Vehicle, NavRecord
from django.db.models import Count, Sum, Avg, Q, DecimalField, F, Case, When, IntegerField, Max, Min, Subquery, OuterRef
from django.db import connection, transaction


# Adding Item view
# /add service; POST
class VehicleView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        vehicles = Vehicle.objects.all()
        if not vehicles:
            raise NotFound('item not found')
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


# Update Item View
# /Update service;POST
class UpdateVehicleView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        id = request.data['vehicle_id']
        qs = Vehicle.objects.filter(vehicle_id=id).first()
        serializer = VehicleSerializer(qs, data=data)

        if qs is None:
            raise NotFound('Vehicle not found')

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class AddNavRecordView(APIView):
    def post(self, request):
        serializer = NavigationRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        nav_record = NavRecord.objects.all()
        if not nav_record:
            raise NotFound('navigation record not found')
        serializer = NavigationRecordSerializer(nav_record, many=True)
        return Response(serializer.data)


class LastPointsView(APIView):
    def get(self, request):
        """
        # raw SQL might be used for group by according to only vehicle_id
        sql='select nav.vehicle_id,nav.latitude,nav.longitude,vec.vehicle_plate,MAX(nav.datetime) ' \
            'from navigation_record_navigationrecord as nav,navigation_record_vehicle as vec ' \
            'where nav.vehicle_id=vec.vehicle_id Group By vec.vehicle_id'
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        """
        model_max_set = NavRecord.objects.values('vehicle').annotate(max_date=Max('datetime')).order_by()

        q_statement = Q()
        for pair in model_max_set:
            q_statement |= (Q(vehicle__exact=pair['vehicle']) & Q(datetime=pair['max_date']))
        model_set = NavRecord.objects.filter(q_statement).annotate(
            plate=F('vehicle__vehicle_plate')).values('plate', 'datetime', 'latitude', 'longitude')
        # serializer = NavigationRecordSerializer(model_set, many=True)
        return Response(model_set)
