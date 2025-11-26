from rest_framework import serializers
from .models import Station, Route, Train, Stop, Line

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)
    
    class Meta:
        model = Station
        fields = '__all__'

class StopSerializer(serializers.ModelSerializer):
    station_name_fr = serializers.CharField(source='station.name_fr')
    station_name_ar = serializers.CharField(source='station.name_ar')
    
    class Meta:
        model = Stop
        fields = ['station_id', 'station_name_fr', 'station_name_ar', 'arrival_time', 'departure_time', 'sequence']

class TrainSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True, read_only=True)
    route_name = serializers.CharField(source='route.name')
    
    class Meta:
        model = Train
        fields = ['id', 'number', 'route_name', 'days_operational', 'stops']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'
