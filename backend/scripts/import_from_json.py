import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")
django.setup()

from api.models import Station, Route, Train, Stop, Line

def import_from_json(json_file_path):
    """Import train data from the manual JSON file"""
    
    print(f"📂 Reading data from: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    print(f"✅ JSON file loaded successfully")
    
    # Get all existing stations
    station_objs = {s.name_fr: s for s in Station.objects.all()}
    
    # Map route names to route objects
    route_map = {r.name: r for r in Route.objects.all()}
    
    trains_data = data.get('trains', [])
    
    if not trains_data:
        print("⚠️  No trains found in JSON file")
        return
    
    # Filter out example trains
    trains_data = [t for t in trains_data if not t.get('number', '').startswith('EXAMPLE')]
    
    print(f"\n📊 Found {len(trains_data)} trains to import")
    
    imported_count = 0
    skipped_count = 0
    
    for train_data in trains_data:
        train_number = train_data.get('number')
        route_name = train_data.get('route')
        days = train_data.get('days_operational', '[*]')
        stops_data = train_data.get('stops', [])
        
        if not train_number or not route_name:
            print(f"⚠️  Skipping train with missing number or route")
            skipped_count += 1
            continue
        
        if route_name not in route_map:
            print(f"⚠️  Skipping train {train_number}: Route '{route_name}' not found")
            print(f"   Available routes: {list(route_map.keys())}")
            skipped_count += 1
            continue
        
        route = route_map[route_name]
        
        # Check if train already exists
        existing_train = Train.objects.filter(number=train_number, route=route).first()
        if existing_train:
            print(f"ℹ️  Train {train_number} already exists on route {route_name}, updating...")
            train = existing_train
            # Clear existing stops
            train.stops.all().delete()
        else:
            train = Train.objects.create(
                number=train_number,
                route=route,
                days_operational=days
            )
            print(f"✅ Created train {train_number} on route {route_name}")
        
        # Add stops
        stops_created = 0
        for seq, stop_data in enumerate(stops_data, 1):
            station_name = stop_data.get('station_name')
            time_str = stop_data.get('time')
            
            if not station_name or not time_str:
                continue
            
            if station_name not in station_objs:
                print(f"   ⚠️  Warning: Station '{station_name}' not found, skipping stop")
                continue
            
            Stop.objects.create(
                train=train,
                station=station_objs[station_name],
                departure_time=time_str,
                sequence=seq
            )
            stops_created += 1
        
        print(f"   ✅ Added {stops_created} stops to train {train_number}")
        imported_count += 1
    
    print(f"\n✅ Import complete!")
    print(f"   Imported: {imported_count} trains")
    print(f"   Skipped: {skipped_count} trains")
    print(f"\n📊 Database stats:")
    print(f"   Total Trains: {Train.objects.count()}")
    print(f"   Total Stops: {Stop.objects.count()}")

if __name__ == "__main__":
    json_path = "/home/mathxro/AntiGrav/train_data.json"
    
    print("=" * 60)
    print("  SNTF Train Data Import from JSON")
    print("=" * 60)
    
    import_from_json(json_path)
    
    print("\n" + "=" * 60)
