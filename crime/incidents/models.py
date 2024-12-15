from django.db import models

class OffenseCategory(models.Model):
    """
    Model for Offense Category eg. Drug & Alcohol
    """
    offense_category_short = models.CharField(max_length = 100) # eg. theft-from-motor-vehicle
    offense_category_name = models.CharField(max_length =200) # eg. Theft from Motor Vehicle

    def __str__(self):
        return self.offense_category_name

class OffenseType(models.Model):
    """
    Model for Offense Type eg. Burglary and auto theft at a residence
    """
    offense_type_short = models.CharField(max_length = 100) # eg. weapon-flourishing
    offense_type_name = models.CharField(max_length = 200) # eg. Flourishing a weapon at another person

    def __str__(self):
        return self.offense_type_name

class Neighbourhood(models.Model):
    """
    Model for Neighbourhood eg. Union Station
    """
    name = models.CharField(max_length=100, default = "No location")

    def __str__(self):
        return self.name

class Geolocation(models.Model):
    """
    Model for Geolocation that contains the geo-coordinates of the incident
    """
    geo_x = models.FloatField(default = 0)
    geo_y = models.FloatField(default = 0)
    geo_lon = models.FloatField(default = 0)
    geo_lat =  models.FloatField(default = 0)


class Location(models.Model):
    """
    Model for Location that contains the details of where the incident took place
    """
    incident_address = models.CharField(max_length = 256) # eg. 8148 PENA BLVD
    district_id = models.IntegerField(default = 0) # eg. 7
    precinct_id = models.IntegerField(default = 0) # eg, 759
    geo = models.ForeignKey(Geolocation, on_delete = models.DO_NOTHING) # Foreign key to Geolocation
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete = models.DO_NOTHING) # Foreign key to Neighbourhood

class Crime(models.Model):
    """
    Model for Crime that contains broad details of the incident
    """
    first_occurrence_date = models.DateTimeField() # eg. 2023-08-14 06:48:00
    reported_date = models.DateTimeField() # eg. 2023-08-14 07:10:00
    is_crime = models.BooleanField() # whether it is a crime
    is_traffic = models.BooleanField() # whether it is related to traffic
    victim_count = models.IntegerField(default = 0) # how many were harmed
    offense_type = models.ForeignKey(OffenseType, on_delete = models.DO_NOTHING) # Foreign key to Offense_type
    offense_category = models.ForeignKey(OffenseCategory, on_delete = models.DO_NOTHING) # Foreign key to Offense_category
