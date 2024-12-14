from rest_framework import serializers
from .models import *

class OffenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenseType
        fields = ['id','offense_type_short','offense_type_name']

class OffenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenseCategory
        fields = ['id','offense_category_short','offense_category_name']

class NeighbourhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbourhood
        fields = ['id','neighbourhood_name']

class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = ['geo_x','geo_y','geo_lon','geo_lat']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['incident_address','district_id','precinct_id','geo','neighbourhood']


    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        geo_data = self.initial_data['geo_id']
        neighbourhood_data = self.initial_data['neighbourhood']

        new_location = Location(**{
            **validated_data,
            'geo_id' : Geolocation.objects.get(pk = geo_data['id']),
            'neighbourhood' : Neighbourhood.objects.get(pk = neighbourhood_data['id'])
        })

        new_location.save()

        return new_location

class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = ['first_occurrence_date','reported_date','is_crime','is_traffic',
                  'victim_count','offense_type','offense_category']

    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        offense_type_data = self.initial_data['offense_type']
        offense_category_data = self.initial_data['offense_category']

        new_crime = Crime(**{
            **validated_data,
            'offense_type' : Crime.objects.get(pk = offense_type_data['id']),
            'offense_category': Crime.objects.get(pk = offense_category_data['id'])
        })

        new_crime.save()

        return new_crime