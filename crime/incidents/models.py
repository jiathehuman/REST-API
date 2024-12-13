from django.db import models
from django.utils import timezone # Django's time-zone utility

class Offense_type(models.Model):
    offense_type_id = models.CharField(max_length = 100, primary_key= False)
    offense_type_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.offense_type_name

class Offense_category(models.Model):
    offense_category_id = models.CharField(max_length = 100, primary_key= False)
    offense_category_name = models.CharField(max_length =200)

    def __str__(self):
        return self.offense_category_name

class Neighbourhood(models.Model):
    neighbourhood_id = models.CharField(max_length=100, default = "No location")

    def __str__(self):
        return self.neighbourhood_id

class Geolocation(models.Model):
    geo_x = models.FloatField(default = 0)
    geo_y = models.FloatField(default = 0)
    geo_lon = models.FloatField(default = 0)
    geo_lat =  models.FloatField(default = 0)

class Location(models.Model):
    incident_address = models.CharField(max_length = 256)
    district_id = models.IntegerField(default = 0)
    precinct_id = models.IntegerField(default = 0)
    geo_id = models.ForeignKey(Geolocation, on_delete = models.DO_NOTHING)
    neighbourhood_id = models.ForeignKey(Neighbourhood, on_delete = models.DO_NOTHING)

class Crime(models.Model):
    first_occurrence_date = models.DateTimeField()
    reported_date = models.DateTimeField()
    is_crime = models.BooleanField()
    is_traffic = models.BooleanField()
    victim_count = models.IntegerField(default = 0)
    offense_type_id = models.ForeignKey(Offense_type, on_delete = models.DO_NOTHING)
    offense_category_id = models.ForeignKey(Offense_category, on_delete = models.DO_NOTHING)
