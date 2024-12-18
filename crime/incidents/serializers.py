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
        fields = '__all__'

class GeolocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Geolocation
    """
    class Meta:
        model = Geolocation
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location
    """
    geo = GeolocationSerializer()
    neighbourhood = NeighbourhoodSerializer()

    class Meta:
        model = Location
        fields = ['id','incident_address','district_id','precinct_id','geo','neighbourhood']

    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        geo_data = validated_data.pop('geo')

        geo_serializer = GeolocationSerializer(data = geo_data)
        geo_serializer.is_valid()
        geo_instance = geo_serializer.save()

        neighbourhood_data = validated_data.pop('neighbourhood')
        neighbourhood, created = Neighbourhood.objects.get_or_create(**neighbourhood_data)


        location = Location.objects.create(
            incident_address = validated_data['incident_address'],
            district_id = validated_data['district_id'],
            precinct_id = validated_data['precinct_id'],
            neighbourhood = neighbourhood,
            geo = geo_instance,
        )

        return location

class CrimeSerializer(serializers.ModelSerializer):
    """
    Serializer for Crime incident
    """
    location = LocationSerializer()

    class Meta:
        model = Crime
        fields = ['id','first_occurrence_date','reported_date','is_crime','is_traffic','location',
                  'victim_count','offense_type','offense_category']


    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        location_data = self.validated_data.pop('location')

        location_serializer = LocationSerializer(data = location_data)
        if location_serializer.is_valid():
            location_instance = location_serializer.save()
        else:
            raise serializers.ValidationError(location_serializer.errors)


        crime = Crime.objects.create(
            first_occurrence_date = validated_data['first_occurrence_date'],
            reported_date = validated_data['reported_date'],
            is_crime = validated_data['is_crime'],
            is_traffic = validated_data['is_traffic'],
            victim_count = validated_data['victim_count'],
            location = location_instance,
            offense_type = validated_data['offense_type'],
            offense_category = validated_data['offense_category']
        )

        return crime


