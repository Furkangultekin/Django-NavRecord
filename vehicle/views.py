from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import VehicleSerializer, NavigationRecordSerializer
from .models import Vehicle, NavRecord
from django.db.models import Q,  F, Max, Min
from django.db import connection, transaction


class AddVehicleView(APIView):
    def post(self, request):
        """
        :request: POST /vehicle/add_vehicle
        :body: {
                "vehicle_id": 1,
                "vehicle_plate":"06 XXX 555"
                }
        """
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetVehicleView(APIView):
    def get(self, request):
        """
        :request: GET /vehicle/get_vehicle
        :response: [
                    {
                        "vehicle_id": 1,
                        "vehicle_plate": "06 XXX 555"
                    },
                    {
                        "vehicle_id": 2,
                        "vehicle_plate": "06 YYY 666"
                    },
                    ...
                 ]
        """
        vehicles = Vehicle.objects.all()
        if not vehicles:
            raise NotFound('Vehicle not found')
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


class UpdateVehicleView(APIView):
    def post(self, request, *args, **kwargs):
        """
        :request: POST /vehicle/update_vehicle
        :body: {
                    "vehicle_id": 3,
                    "vehicle_plate":"06 TTT 777"
                }
        """
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
        """
        :request: POST /vehicle/add_nav_record
        :body:{
                    "vehicle":2,
                    "latitude":30.32,
                    "longitude":35.00
                }
        :response:{
                    "vehicle": 2,
                    "datetime": "2022-05-19T15:36:37.808815Z",
                    "latitude": "30.32",
                    "longitude": "35.00"
                }
        """
        vehicle = request.data['vehicle']
        NavRecord.objects.filter(vehicle=vehicle, latest=1).update(latest=0)
        serializer = NavigationRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetNavRecordView(APIView):
    def get(self, request):
        """
        :request: GET /vehicle/get_nav_record
        :response: [
                        {
                            "vehicle": 2,
                            "datetime": "2022-05-19T15:36:37.808815Z",
                            "latitude": "30.32",
                            "longitude": "35.00"
                        },
                        {
                            "vehicle": 2,
                            "datetime": "2022-05-19T15:37:15.037388Z",
                            "latitude": "33.33",
                            "longitude": "36.00"
                        },
                        ...
                    ]
        """
        nav_record = NavRecord.objects.all()
        if not nav_record:
            raise NotFound('navigation record not found')
        serializer = NavigationRecordSerializer(nav_record, many=True)
        return Response(serializer.data)


class LastPointsView(APIView):
    def get(self, request):
        """
        :request: GET /vehicle/last_nav_record
        :response: [
                        {
                            "datetime": "2022-05-19T15:37:46.804969Z",
                            "latitude": 24.25,
                            "longitude": 26.0,
                            "plate": "06 XXX 555"
                        },
                        {
                            "datetime": "2022-05-19T15:37:25.773796Z",
                            "latitude": 37.33,
                            "longitude": 35.0,
                            "plate": "06 YYY 666"
                        },
                        {
                            "datetime": "2022-05-19T15:38:06.662713Z",
                            "latitude": 41.25,
                            "longitude": 48.0,
                            "plate": "06 TTT 777"
                        }
                    ]
        """
        """
        # raw SQL might be used for group by according to only vehicle_id

        sql='select nav.vehicle_id,nav.latitude,nav.longitude,vec.vehicle_plate,MAX(nav.datetime) ' \
            'from vehicle_navrecord as nav,vehicle_vehicle as vec ' \
            'where nav.vehicle_id=vec.vehicle_id Group By vec.vehicle_id'

        cursor = connection.cursor()
        cursor.execute(sql)
        model_set = cursor.fetchall()
        """

        """
        # query without "latest" column
        # searhing for each vehicle and max_date
        
        model_max_set = NavRecord.objects.values('vehicle').annotate(max_date=Max('datetime')).order_by()

        q_statement = Q()
        for pair in model_max_set:
            q_statement |= (Q(vehicle__exact=pair['vehicle']) & Q(datetime=pair['max_date']))
        model_set = NavRecord.objects.filter(q_statement).annotate(
            plate=F('vehicle__vehicle_plate')).values('plate', 'datetime', 'latitude', 'longitude')
        """

        # after adding latest boolean column our query:
        model_set = NavRecord.objects.filter(latest=1).annotate(
            plate=F('vehicle__vehicle_plate')
            ).values('plate', 'datetime', 'latitude', 'longitude').order_by()

        return Response(model_set)
