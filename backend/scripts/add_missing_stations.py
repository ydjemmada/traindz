import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")
django.setup()

from api.models import Station, Line

def add_missing_stations():
    """Add stations that were in the Excel but not in the database"""
    
    # Get the Alger-Thenia line
    line_at = Line.objects.get(code="AT")
    line_ae = Line.objects.get(code="AE")
    
    # Missing stations from the Oued Aissi extension (beyond Thenia)
    oued_aissi_stations = [
        {"name_fr": "Thénia", "name_ar": "الثنية"},  # Alternate spelling
        {"name_fr": "Si Mustapha", "name_ar": "سي مصطفى"},
        {"name_fr": "Isser", "name_ar": "يسر"},
        {"name_fr": "Bordj Menaïel", "name_ar": "برج منايل"},
        {"name_fr": "Naciria", "name_ar": "الناصرية"},
        {"name_fr": "Tadmaït", "name_ar": "تادمايت"},
        {"name_fr": "Draâ Ben Khedda", "name_ar": "ذراع بن خدة"},
        {"name_fr": "Boukhalfa", "name_ar": "بوخالفة"},
        {"name_fr": "Tizi Ouzou", "name_ar": "تيزي وزو"},
        {"name_fr": "Kef Naâdja", "name_ar": "الكاف نعجة"},
        {"name_fr": "Oued Aïssi (Université)", "name_ar": "وادي عيسى (الجامعة)"},
        {"name_fr": "Oued Aïssi", "name_ar": "وادي عيسى"},
        {"name_fr": "Boumerdès", "name_ar": "بومرداس"},  # Alternate spelling
        {"name_fr": "Réghaïa", "name_ar": "رغاية"},  # Alternate spelling
    ]
    
    # Missing station abbreviations
    abbreviations = [
        {"name_fr": "B.Mered", "name_ar": "بني مراد"},  # Abbreviation for Beni Mered
        {"name_fr": "Gué de Cne", "name_ar": "جسر قسنطينة"},  # Abbreviation for Gué de Constantine
    ]
    
    print("Adding missing stations...")
    
    stations_added = 0
    
    # Check for Thénia vs Thenia
    if not Station.objects.filter(name_fr="Thénia").exists():
        # Map Thénia to Thenia (they're the same)
        print(f"Note: 'Thénia' is same as 'Thenia', will use existing station")
    
    # Check for Boumerdès vs Boumerdes
    if not Station.objects.filter(name_fr="Boumerdès").exists():
        print(f"Note: 'Boumerdès' is same as 'Boumerdes', will use existing station")
    
    # Check for Réghaïa vs Reghaia
    if not Station.objects.filter(name_fr="Réghaïa").exists():
        print(f"Note: 'Réghaïa' is same as 'Reghaia', will use existing station")
    
    # Add Oued Aissi extension stations (if they don't exist)
    for station_data in oued_aissi_stations:
        name = station_data["name_fr"]
        
        # Skip if it's a variant of existing station
        if name in ["Thénia", "Boumerdès", "Réghaïa"]:
            continue
        
        if not Station.objects.filter(name_fr=name).exists():
            s = Station.objects.create(
                name_fr=name,
                name_ar=station_data["name_ar"],
                line=line_at
            )
            print(f"✅ Added station: {name}")
            stations_added += 1
        else:
            print(f"ℹ️  Station already exists: {name}")
    
    # Add abbreviations as mappings (we'll update the import script to handle these)
    for abbr in abbreviations:
        name = abbr["name_fr"]
        if not Station.objects.filter(name_fr=name).exists():
            s = Station.objects.create(
                name_fr=name,
                name_ar=abbr["name_ar"],
                line=line_ae
            )
            print(f"✅ Added station abbreviation: {name}")
            stations_added += 1
    
    print(f"\n✅ Added {stations_added} new stations")
    print(f"📊 Total stations now: {Station.objects.count()}")

if __name__ == "__main__":
    add_missing_stations()
