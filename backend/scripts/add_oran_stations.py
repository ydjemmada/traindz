import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")
django.setup()

from api.models import Station, Route, Line

def add_oran_line_stations():
    """Add stations for the Alger-Oran intercity line"""
    
    # Get or create the Alger-Oran line
    line_ao, _ = Line.objects.get_or_create(
        code='AO',
        defaults={'name': 'Alger - Oran'}
    )
    
    # Complete list of stations on the Alger-Oran line (from the Excel)
    # I'll list all stations visible in the data
    oran_stations = [
        {"name_fr": "Khemis Miliana", "name_ar": "خميس مليانة"},
        {"name_fr": "Arib", "name_ar": "عريب"},
        {"name_fr": "Ain Defla", "name_ar": "عين الدفلى"},
        {"name_fr": "Rouina", "name_ar": "رويينة"},
        {"name_fr": "El Attaf", "name_ar": "العطاف"},
        {"name_fr": "Oued Fodda", "name_ar": "وادي الفضة"},
        {"name_fr": "Chlef", "name_ar": "الشلف"},
        {"name_fr": "Oued Sly", "name_ar": "وادي سلي"},
        {"name_fr": "Relizane", "name_ar": "غليزان"},
        {"name_fr": "Zemmoura", "name_ar": "زمورة"},
        {"name_fr": "Sidi Bel Abbes", "name_ar": "سيدي بلعباس"},
        {"name_fr": "Sfisef", "name_ar": "صفيصف"},
        {"name_fr": "Oran", "name_ar": "وهران"},
    ]
    
    print("Adding Oran line stations...")
    stations_added = 0
    
    for station_data in oran_stations:
        name = station_data["name_fr"]
        
        if not Station.objects.filter(name_fr=name).exists():
            s = Station.objects.create(
                name_fr=name,
                name_ar=station_data["name_ar"],
                line=line_ao
            )
            print(f"✅ Added station: {name}")
            stations_added += 1
        else:
            print(f"ℹ️  Station already exists: {name}")
    
    # Create routes
    alger = Station.objects.filter(name_fr='Alger').first()
    oran = Station.objects.filter(name_fr='Oran').first()
    
    if alger and oran:
        route_ao, created = Route.objects.get_or_create(
            name="Alger - Oran",
            defaults={
                'origin': alger,
                'destination': oran,
                'line': line_ao
            }
        )
        if created:
            print(f"✅ Created route: {route_ao.name}")
        
        route_oa, created = Route.objects.get_or_create(
            name="Oran - Alger",
            defaults={
                'origin': oran,
                'destination': alger,
                'line': line_ao
            }
        )
        if created:
            print(f"✅ Created route: {route_oa.name}")
    
    print(f"\n✅ Added {stations_added} new stations")
    print(f"📊 Total stations now: {Station.objects.count()}")
    print(f"📊 Total routes now: {Route.objects.count()}")

if __name__ == "__main__":
    add_oran_line_stations()
