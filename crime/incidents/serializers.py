from rest_framework import serializers
from .models import *

class Offense_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offense_type
        fields = ['id','offense_type_short','offense_type_name']

class Offense_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Offense_category
        fields = ['id','offense_category_short','offense_category_name']

class NeighbourhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbourhood
        fields = ['id','neighbourhood_id']


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = ['id','geo_x','geo_y','geo_lon','geo_lat']

class LocationSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = ['incident_address','district_id','precinct_id',
                  'geo_id','neighbourhood_id']
    incident_address = serializers.CharField(required = True, allow_blank = True, max_length = 256)
    district_id = serializers.IntegerField(default = 0)
    precinct_id = serializers.IntegerField(default = 0)


    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        geo_data = self.initial_data['geo_id']
        neighbourhood_data = self.initial_data['neighbourhood_id']

        new_location = Location(**{
            **validated_data,
            'geo_id' : Geolocation.objects.get(pk = geo_data['id']),
            'neighbourhood_id' : Neighbourhood.objects.get(pk = neighbourhood_data['id'])
        })

        new_location.save()

        return new_location

    def update(self, instance, validated_data):
        """
        Update and return an existing `Location` instance, given the validated data
        """

class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = ['first_occurrence_date','reported_date','is_crime','is_traffic',
                  'victim_count','offense_type_id','offense_category_id']

    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        offense_type_data = self.initial_data['offense_type_id']
        offense_category_data = self.initial_data['offense_category_id']

        new_crime = Crime(**{
            **validated_data,
            'offense_type_id' : Crime.objects.get(pk = offense_type_data['id']),
            'offense_category_id': Crime.objects.get(pk = offense_category_data['id'])
        })

        new_crime.save()

        return new_crime