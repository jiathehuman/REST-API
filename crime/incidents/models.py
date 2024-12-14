from django.db import models
from django.utils import timezone # Django's time-zone utility

class OffenseType(models.Model):
    offense_type_short = models.CharField(max_length = 100)
    offense_type_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.offense_type_name

class OffenseCategory(models.Model):
    offense_category_short = models.CharField(max_length = 100)
    offense_category_name = models.CharField(max_length =200)

    def __str__(self):
        return self.offense_category_name

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100, default = "No location")

    def __str__(self):
        return self.name

class Geolocation(models.Model):
    geo_x = models.FloatField(default = 0)
    geo_y = models.FloatField(default = 0)
    geo_lon = models.FloatField(default = 0)
    geo_lat =  models.FloatField(default = 0)

class Location(models.Model):
    incident_address = models.CharField(max_length = 256)
    district_id = models.IntegerField(default = 0)
    precinct_id = models.IntegerField(default = 0)
    geo = models.ForeignKey(Geolocation, on_delete = models.DO_NOTHING)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete = models.DO_NOTHING)

class Crime(models.Model):
    first_occurrence_date = models.DateTimeField()
    reported_date = models.DateTimeField()
    is_crime = models.BooleanField()
    is_traffic = models.BooleanField()
    victim_count = models.IntegerField(default = 0)
    offense_type = models.ForeignKey(OffenseType, on_delete = models.DO_NOTHING)
    offense_category = models.ForeignKey(OffenseCategory, on_delete = models.DO_NOTHING)
