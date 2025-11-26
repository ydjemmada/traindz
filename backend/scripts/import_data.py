import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")
django.setup()

from api.models import Station, Route, Train, Stop, Line

def import_structured_data():
    print("Importing structured timetable data...")
    
    # Station data with Arabic names
    stations_data = [
        {"name_fr": "Alger", "name_ar": "الجزائر"},
        {"name_fr": "Agha", "name_ar": "آغا"},
        {"name_fr": "Ateliers", "name_ar": "الورشات"},
        {"name_fr": "Hussein Dey", "name_ar": "حسين داي"},
        {"name_fr": "Caroubier", "name_ar": "خروبة"},
        {"name_fr": "El Harrach", "name_ar": "الحراش"},
        {"name_fr": "Oued Smar", "name_ar": "وادي السمار"},
        {"name_fr": "Bab Ezzouar", "name_ar": "باب الزوار"},
        {"name_fr": "Dar El Beida", "name_ar": "الدار البيضاء"},
        {"name_fr": "Rouiba", "name_ar": "رويبة"},
        {"name_fr": "Rouiba Ind", "name_ar": "رويبة صناعية"},
        {"name_fr": "Rouiba SNVI", "name_ar": "رويبة صناعية"},
        {"name_fr": "Reghaia", "name_ar": "رغاية"},
        {"name_fr": "Reghaia Ind", "name_ar": "رغاية صناعية"},
        {"name_fr": "Boudouaou", "name_ar": "بودواو"},
        {"name_fr": "Boumerdes", "name_ar": "بومرداس"},
        {"name_fr": "Tidjelabine", "name_ar": "تيجيلابين"},
        {"name_fr": "Thenia", "name_ar": "الثنية"},
        {"name_fr": "Gué de Constantine", "name_ar": "جسر قسنطينة"},
        {"name_fr": "Ain Naadja", "name_ar": "عين النعجة"},
        {"name_fr": "Baba Ali", "name_ar": "بابا علي"},
        {"name_fr": "Birtouta", "name_ar": "بئر توتة"},
        {"name_fr": "Boufarik", "name_ar": "بوفاريك"},
        {"name_fr": "Beni Mered", "name_ar": "بني مراد"},
        {"name_fr": "Blida", "name_ar": "البليدة"},
        {"name_fr": "Chiffa", "name_ar": "شفة"},
        {"name_fr": "Mouzaia", "name_ar": "موزاية"},
        {"name_fr": "El Affroun", "name_ar": "العفون"},
        {"name_fr": "Tessala El Merdja", "name_ar": "تسالة المرجة"},
        {"name_fr": "Sidi Abdelah", "name_ar": "سيدي عبد الله"},
        {"name_fr": "Zéralda", "name_ar": "زرالدة"},
        {"name_fr": "Aeroport Houari Boumediene", "name_ar": "مطار هواري بومدين"},
        {"name_fr": "Corso", "name_ar": "قورصو"},
    ]
    
    # Create Lines
    line_at, _ = Line.objects.get_or_create(name="Alger - Thenia", code="AT")
    line_ae, _ = Line.objects.get_or_create(name="Alger - El Affroun", code="AE")
    line_az, _ = Line.objects.get_or_create(name="Alger - Zéralda", code="AZ")
    line_ap, _ = Line.objects.get_or_create(name="Airport Line", code="AP")
    
    # Create/Update stations with Arabic names
    station_objs = {}
    for idx, station_data in enumerate(stations_data):
        s, created = Station.objects.update_or_create(
            name_fr=station_data["name_fr"],
            defaults={'name_ar': station_data["name_ar"]}
        )
        station_objs[station_data["name_fr"]] = s
        if created:
            print(f"Created station: {station_data['name_fr']} / {station_data['name_ar']}")
        else:
            print(f"Updated station: {station_data['name_fr']} with Arabic name")
    
    # Assign lines to stations
    at_stations = ["Alger", "Agha", "Ateliers", "Hussein Dey", "Caroubier", "El Harrach",
                   "Oued Smar", "Bab Ezzouar", "Dar El Beida", "Rouiba", "Rouiba Ind",
                   "Rouiba SNVI", "Reghaia", "Reghaia Ind", "Boudouaou", "Corso",
                   "Boumerdes", "Tidjelabine", "Thenia"]
    
    ae_stations = ["Alger", "Agha", "Ateliers", "Hussein Dey", "Caroubier", "El Harrach",
                   "Gué de Constantine", "Ain Naadja", "Baba Ali", "Birtouta", "Boufarik",
                   "Beni Mered", "Blida", "Chiffa", "Mouzaia", "El Affroun"]
    
    az_stations = ["Alger", "Agha", "Ateliers", "Hussein Dey", "Caroubier", "El Harrach",
                   "Gué de Constantine", "Ain Naadja", "Baba Ali", "Birtouta",
                   "Tessala El Merdja", "Sidi Abdelah", "Zéralda"]
    
    ap_stations = ["Agha", "El Harrach", "Bab Ezzouar", "Aeroport Houari Boumediene"]
    
    for s in at_stations:
        if s in station_objs:
            station_objs[s].line = line_at
            station_objs[s].save()
    
    # Create Routes
    route_at = Route.objects.get_or_create(
        name="Alger - Thenia",
        defaults={'origin': station_objs["Alger"], 'destination': station_objs["Thenia"], 'line': line_at}
    )[0]
    
    route_ta = Route.objects.get_or_create(
        name="Thenia - Alger",
        defaults={'origin': station_objs["Thenia"], 'destination': station_objs["Alger"], 'line': line_at}
    )[0]
    
    route_ae = Route.objects.get_or_create(
        name="Alger - El Affroun",
        defaults={'origin': station_objs["Alger"], 'destination': station_objs["El Affroun"], 'line': line_ae}
    )[0]
    
    route_ea = Route.objects.get_or_create(
        name="El Affroun - Alger",
        defaults={'origin': station_objs["El Affroun"], 'destination': station_objs["Alger"], 'line': line_ae}
    )[0]
    
    route_az = Route.objects.get_or_create(
        name="Alger - Zéralda",
        defaults={'origin': station_objs["Alger"], 'destination': station_objs["Zéralda"], 'line': line_az}
    )[0]
    
    route_za = Route.objects.get_or_create(
        name="Zéralda - Alger",
        defaults={'origin': station_objs["Zéralda"], 'destination': station_objs["Alger"], 'line': line_az}
    )[0]
    
    route_ap = Route.objects.get_or_create(
        name="Agha - Aeroport",
        defaults={'origin': station_objs["Agha"], 'destination': station_objs["Aeroport Houari Boumediene"], 'line': line_ap}
    )[0]
    
    # Import Train Schedules - Alger-Thenia
    trains_at = [
        {
            "number": "27", "days": "[1]", "route": route_at,
            "stops": [
                ("Alger", "06:20"), ("Agha", "06:23"), ("Ateliers", "06:26"), ("Hussein Dey", "06:30"),
                ("Caroubier", "06:33"), ("El Harrach", "06:36"), ("Bab Ezzouar", "06:47"),
                ("Dar El Beida", "06:47"), ("Rouiba", "06:52"), ("Reghaia", "06:57"),
                ("Boumerdes", "07:10"), ("Tidjelabine", "07:14"), ("Thenia", "07:19")
            ]
        },
        {
            "number": "33", "days": "[*]", "route": route_at,
            "stops": [
                ("Alger", "07:30"), ("Agha", "07:33"), ("Ateliers", "07:37"), ("Hussein Dey", "07:41"),
                ("Caroubier", "07:44"), ("El Harrach", "07:47"), ("Oued Smar", "07:53"),
                ("Bab Ezzouar", "07:56"), ("Dar El Beida", "08:00"), ("Rouiba", "08:05"),
                ("Rouiba Ind", "08:07"), ("Reghaia Ind", "08:09"), ("Reghaia", "08:10"),
                ("Boudouaou", "08:13"), ("Corso", "08:16"), ("Boumerdes", "08:20"),
                ("Tidjelabine", "08:24"), ("Thenia", "08:29")
            ]
        },
        {
            "number": "35", "days": "[*]", "route": route_at,
            "stops": [
                ("Alger", "08:30"), ("Agha", "08:33"), ("Ateliers", "08:36"), ("Hussein Dey", "08:40"),
                ("Caroubier", "08:43"), ("El Harrach", "08:46"), ("Oued Smar", "08:51"),
                ("Bab Ezzouar", "08:54"), ("Dar El Beida", "08:57"), ("Rouiba", "09:02"),
                ("Boudouaou", "09:13"), ("Corso", "09:16"), ("Boumerdes", "09:20"),
                ("Tidjelabine", "09:24"), ("Thenia", "09:29")
            ]
        },
    ]
    
    # Import Train Schedules - Thenia-Alger
    trains_ta = [
        {
            "number": "22", "days": "[1]", "route": route_ta,
            "stops": [
                ("Thenia", "06:00"), ("Tidjelabine", "06:04"), ("Boumerdes", "06:08"),
                ("Boudouaou", "06:15"), ("Reghaia", "06:21"), ("Rouiba", "06:26"),
                ("Dar El Beida", "06:32"), ("Bab Ezzouar", "06:35"), ("Oued Smar", "06:39"),
                ("El Harrach", "06:44"), ("Caroubier", "06:47"), ("Hussein Dey", "06:50"),
                ("Ateliers", "06:54"), ("Agha", "06:57"), ("Alger", "07:02")
            ]
        },
    ]
    
    # Import Train Schedules - Alger-El Affroun
    trains_ae = [
        {
            "number": "1025", "days": "[1]", "route": route_ae,
            "stops": [
                ("Alger", "05:35"), ("Agha", "05:38"), ("Ateliers", "05:41"), ("Hussein Dey", "05:45"),
                ("Caroubier", "05:48"), ("El Harrach", "05:51"), ("Gué de Constantine", "05:56"),
                ("Ain Naadja", "05:59"), ("Baba Ali", "06:03"), ("Birtouta", "06:08"),
                ("Boufarik", "06:16"), ("Beni Mered", "06:22"), ("Blida", "06:28"),
                ("Chiffa", "06:35"), ("Mouzaia", "06:39"), ("El Affroun", "06:44")
            ]
        },
    ]
    
    # Import Airport trains
    trains_ap = [
        {
            "number": "B609", "days": "[*]", "route": route_ap,
            "stops": [
                ("Agha", "04:40"), ("El Harrach", "04:49"), ("Bab Ezzouar", "04:56"),
                ("Aeroport Houari Boumediene", "05:00")
            ]
        },
        {
            "number": "B611", "days": "[*]", "route": route_ap,
            "stops": [
                ("Agha", "06:00"), ("El Harrach", "06:09"), ("Bab Ezzouar", "06:16"),
                ("Aeroport Houari Boumediene", "06:20")
            ]
        },
    ]
    
    all_trains = trains_at + trains_ta + trains_ae + trains_ap
    
    for train_data in all_trains:
        train, created = Train.objects.get_or_create(
            number=train_data["number"],
            route=train_data["route"],
            defaults={'days_operational': train_data["days"]}
        )
        
        if created:
            print(f"Created train {train_data['number']}")
        
        # Clear existing stops for this train
        train.stops.all().delete()
        
        for seq, (station_name, time_str) in enumerate(train_data["stops"], 1):
            if station_name in station_objs:
                Stop.objects.create(
                    train=train,
                    station=station_objs[station_name],
                    departure_time=time_str,
                    sequence=seq
                )
    
    print(f"\n✅ Import complete!")
    print(f"   Stations: {Station.objects.count()}")
    print(f"   Lines: {Line.objects.count()}")
    print(f"   Routes: {Route.objects.count()}")
    print(f"   Trains: {Train.objects.count()}")
    print(f"   Stops: {Stop.objects.count()}")

if __name__ == "__main__":
    # Clear old data
    Stop.objects.all().delete()
    Train.objects.all().delete()
    
    import_structured_data()
