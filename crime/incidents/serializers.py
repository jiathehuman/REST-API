from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class OffenseTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for Offense Type
    """
    class Meta:
        model = OffenseType
        fields = ['id','offense_type_short','offense_type_name']


class OffenseCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Offense Category
    """
    class Meta:
        model = OffenseCategory
        fields = ['id','offense_category_short','offense_category_name']

class NeighbourhoodSerializer(serializers.ModelSerializer):
    """
    Serializer for Neighbourhood
    """
    class Meta:
        model = Neighbourhood
        fields = ['id','name']
        owner = serializers.ReadOnlyField(source = 'owner.username')

class GeolocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Geolocation
    """
    class Meta:
        model = Geolocation
        fields = ['id','geo_x','geo_y','geo_lon','geo_lat']

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location
    """
    class Meta:
        model = Location
        fields = ['id','incident_address','district_id','precinct_id','geo','neighbourhood']


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
    """
    Serializer for Crime incident
    """
    class Meta:
        model = Crime
        fields = ['id','first_occurrence_date','reported_date','is_crime','is_traffic',
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

class UserSerializer(serializers.ModelSerializer):
    crimes = serializers.PrimaryKeyRelatedField(many = True, queryset = Crime.objects.all())

    class Meta:
        model = User
        fields = ['id','username','snippets']

