from rest_framework import serializers
from incidents.models import *

class Offense_typeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    offense_type_short = serializers.CharField(required = True, allow_blank = False, max_length = 100)
    offense_type_name = serializers.CharField(required = True, allow_blank = False, max_length = 200)

class Offense_categorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    offense_category_short = serializers.CharField(required = True, allow_blank = False, max_length = 100)
    offense_category_name = serializers.CharField(required = True, allow_blank = False, max_length = 200)


class NeighbourhoodSerializer(serializers.Serializer):
    neighbourhood_id = serializers.IntegerField(required = True, default = "No location")


class GeolocationSerializer(serializers.Serializer):
    geo_x = serializers.FloatField(required = True, allow_blank = True)
    geo_y = serializers.FloatField(required = True, allow_blank = True)
    geo_lon = serializers.FloatField(required = True, allow_blank = True)
    geo_lat = serializers.FloatField(required = True, allow_blank = True)

class LocationSerializer(serializers.Serializer):
    incident_address = serializers.CharField(required = True, allow_blank = True, max_length = 256)
    district_id = serializers.IntegerField(default = 0)
    precinct_id = serializers.IntegerField(default = 0)

    geolocat = GeolocationSerializer()
    neighbourhd = NeighbourhoodSerializer()

    # def create(self, validated_data):
        # geo

    # geo_id = models.ForeignKey(Geolocation, on_delete = models.DO_NOTHING)
    # neighbourhood_id = models.ForeignKey(Neighbourhood, on_delete = models.DO_NOTHING)

# class Crime(models.Model):
#     first_occurrence_date = models.DateTimeField()
#     reported_date = models.DateTimeField()
#     is_crime = models.BooleanField()
#     is_traffic = models.BooleanField()
#     victim_count = models.IntegerField(default = 0)
#     offense_type_id = models.ForeignKey(Offense_type, on_delete = models.DO_NOTHING)
#     offense_category_id = models.ForeignKey(Offense_category, on_delete = models.DO_NOTHING)