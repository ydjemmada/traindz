from django.db import models

class Line(models.Model):
    name = models.CharField(max_length=200) # e.g., "Alger - Thenia"
    code = models.CharField(max_length=50, blank=True) # e.g., "AT"
    
    def __str__(self):
        return self.name

class Station(models.Model):
    name_fr = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True, related_name='stations')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    line_connections = models.JSONField(default=list, blank=True) # List of connected line IDs
    
    def __str__(self):
        return f"{self.name_fr} / {self.name_ar}"

class Route(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='routes', null=True)
    origin = models.ForeignKey(Station, related_name='routes_from', on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name='routes_to', on_delete=models.CASCADE)
    name = models.CharField(max_length=200) # e.g., "Alger - Thénia"

    def __str__(self):
        return self.name

class Train(models.Model):
    OPERATING_DAYS_CHOICES = [
        ('daily', 'Daily [*]'),
        ('no_friday', 'No Friday [1]'),
        ('friday_only', 'Friday Only [2]'),
    ]

    number = models.CharField(max_length=50, db_index=True) # e.g., "105", "B152"
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    days_operational = models.CharField(max_length=100, default="Daily") # Keep for legacy/display
    operating_days = models.CharField(max_length=20, choices=OPERATING_DAYS_CHOICES, default='daily', db_index=True)
    active_status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Train {self.number} ({self.route})"

class Stop(models.Model):
    train = models.ForeignKey(Train, related_name='stops', on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True)
    arrival_time = models.TimeField(null=True, blank=True, db_index=True)
    departure_time = models.TimeField(null=True, blank=True, db_index=True)
    sequence = models.IntegerField() # Order of the stop

    class Meta:
        ordering = ['sequence']
        indexes = [
            models.Index(fields=['station', 'departure_time']),
        ]

    def __str__(self):
        return f"{self.train} at {self.station} ({self.departure_time})"

class Connection(models.Model):
    from_station = models.ForeignKey(Station, related_name='connections_from', on_delete=models.CASCADE)
    to_station = models.ForeignKey(Station, related_name='connections_to', on_delete=models.CASCADE)
    transfer_station = models.ForeignKey(Station, related_name='transfers', on_delete=models.CASCADE)
    transfer_time_minutes = models.IntegerField()
    connection_type = models.CharField(max_length=50, default='standard') # standard, optimized
    
    class Meta:
        indexes = [
            models.Index(fields=['from_station', 'to_station']),
        ]
