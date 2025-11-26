import os
import sys
import django
import time
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")
django.setup()

from api.models import Station, Route, Train, Stop
from api.views import find_direct_trains, find_connection_trains

def run_validation():
    print("=" * 60)
    print("  SNTF System Validation Protocol")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Database Integrity
    print("\n🔍 Checking Database Integrity...")
    
    train_count = Train.objects.count()
    stop_count = Stop.objects.count()
    station_count = Station.objects.count()
    
    print(f"   Trains: {train_count}")
    print(f"   Stops: {stop_count}")
    print(f"   Stations: {station_count}")
    
    if train_count == 0: errors.append("No trains found in database")
    if stop_count == 0: errors.append("No stops found in database")
    
    # Check for trains without stops
    empty_trains = []
    for t in Train.objects.all():
        if t.stops.count() == 0:
            empty_trains.append(t.number)
    
    if empty_trains:
        warnings.append(f"Found {len(empty_trains)} trains without stops: {empty_trains[:5]}...")
    else:
        print("   ✅ All trains have stops")
        
    # 2. Search Logic Verification
    print("\n🔍 Verifying Search Logic...")
    
    try:
        alger = Station.objects.get(name_fr='Alger')
        thenia = Station.objects.get(name_fr='Thenia')
        zeralda = Station.objects.get(name_fr='Zéralda')
        
        # Test Direct: Alger -> Thenia
        start_time = time.time()
        direct_results = find_direct_trains(alger, thenia)
        duration = (time.time() - start_time) * 1000
        
        if direct_results:
            print(f"   ✅ Direct Search (Alger->Thenia): Found {len(direct_results)} trains in {duration:.2f}ms")
        else:
            errors.append("Direct search Alger->Thenia returned no results")
            
        # Test Connection: Thenia -> Zeralda (via Alger)
        start_time = time.time()
        conn_results = find_connection_trains(thenia, zeralda)
        duration = (time.time() - start_time) * 1000
        
        if conn_results:
            print(f"   ✅ Connection Search (Thenia->Zeralda): Found {len(conn_results)} options in {duration:.2f}ms")
        else:
            warnings.append("Connection search Thenia->Zeralda returned no results (might be valid if no schedule matches)")

    except Station.DoesNotExist:
        errors.append("Critical stations (Alger, Thenia, Zeralda) not found")
        
    # 3. Operating Day Compliance
    print("\n🔍 Verifying Operating Day Compliance...")
    
    # Find a 'No Friday' train
    no_friday_train = Train.objects.filter(operating_days='no_friday').first()
    if no_friday_train:
        print(f"   Testing with Train {no_friday_train.number} (No Friday)")
        # This is a logic check we'd do via API, but here we check the model data
        if '[1]' in no_friday_train.days_operational:
             print("   ✅ Train correctly marked as [1] in legacy field")
        else:
             warnings.append(f"Train {no_friday_train.number} has operating_days='no_friday' but days_operational='{no_friday_train.days_operational}'")
    else:
        warnings.append("No 'No Friday' trains found to test")

    # 4. Performance Check
    print("\n🔍 Performance Benchmarks...")
    # (Already measured above)
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("❌ VALIDATION FAILED")
        for e in errors: print(f"   - {e}")
    elif warnings:
        print("⚠️  VALIDATION PASSED WITH WARNINGS")
        for w in warnings: print(f"   - {w}")
    else:
        print("✅ SYSTEM VALIDATION PASSED")
    print("=" * 60)

if __name__ == "__main__":
    run_validation()
