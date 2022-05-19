# Django-NavRecord

It is a basic django backend project named NavigationRecord  that keeps vehicles and their locations.

## README Table of Content
- Project Set-up
- Django Application
- REST api requests and responses
- Suggestions

## Project Set-up

After downloading the project, run the commands below in the project folder, respectively:
```
$ python -m venv venv
```
```
$ venv/Scripts/activate
```
```
$ python manage.py runserver
```
## Django Application

  The project named NavigationRecord includes following app:
  - vehicle : It is includes two models; NavRecord and Vehicle. Add, Get and Update operations can be applied to them.

## REST api requests and responses:
### Add new vehicle: 
#### -POST /vehicle/add_vehicle
##### Request:
```
{
    "vehicle_id": 1,
    "vehicle_plate":"06 XXX 555"
}
```

### Get all vehicles:
#### -GET /vehicle/get_vehicle
##### Results:
```
[
    {
        "vehicle_id": 1,
        "vehicle_plate": "06 XXX 555"
    },
    {
        "vehicle_id": 2,
        "vehicle_plate": "06 YYY 666"
    },
    {
        "vehicle_id": 3,
        "vehicle_plate": "06 ZZZ 777"
    }
]
```

### Update a vehicle:
#### -POST /vehicle/update_vehicle
##### Request:
```
{
    "vehicle_id": 3,
    "vehicle_plate":"06 TTT 777"
}
```
##### Result:
```
{
    "vehicle_id": 3,
    "vehicle_plate":"06 TTT 777"
}
```


### Add new navigation record:
#### -POST /vehicle/add_nav_record
##### Request:
```
{
    "vehicle":2,
    "latitude":30.32,
    "longitude":35.00
}
```
#### Result:
```
{
    "vehicle": 2,
    "datetime": "2022-05-19T15:36:37.808815Z",
    "latitude": "30.32",
    "longitude": "35.00"
}
```
### Get all navigation Records:
#### -GET /vehicle/get_nav_record
##### Results:
```
[
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
    {
        "vehicle": 2,
        "datetime": "2022-05-19T15:37:25.773796Z",
        "latitude": "37.33",
        "longitude": "35.00"
    },
    {
        "vehicle": 1,
        "datetime": "2022-05-19T15:37:36.804822Z",
        "latitude": "22.22",
        "longitude": "23.00"
    },
    {
        "vehicle": 1,
        "datetime": "2022-05-19T15:37:46.804969Z",
        "latitude": "24.25",
        "longitude": "26.00"
    },
    {
        "vehicle": 3,
        "datetime": "2022-05-19T15:38:06.662713Z",
        "latitude": "41.25",
        "longitude": "48.00"
    }
]
```
### Listing last navigation record of each vehicle:
#### -GET /vehicle/last_nav_record
##### Results:
```
[
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
```

## Suggestions

1- In the project proposed model structure: 

### Vehicle
| vehicle_id    | PK        |
|:------------- | :---------|
| vehicle_plate | CharField |

### Navigation Record
| id            | PK           |
|:------------- | :----------- |
| vehicle_id    | FK           |
| datetime      | DatetimField |
| latitude      | FloatField   |
| longitude     | FloatField   |
| latest        | BooleanField |

Instead of searhing max_date for each vehicle, usage of latest column might be effective. In the case of adding new navigation record, first we need to update latest column of the last record of the vehicle to 0 and then the new record must be added to table with "latest=1" (check AddNavRecordView). So, we can filter all last points with latest=1 argument (check LastPointsView). In this way, only one connection to the database is established in a view.

2- Adding index concurrently.

3- In-memory databases like Redis to achieve higher performance.

4- GeoDjango can be used to make geo-spatial analysis, queries and manipulation for location-based data








