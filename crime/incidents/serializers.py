from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class OffenseTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for Offense Type
    """
    class Meta:
        model = OffenseType # use the OffenseType model as defined in models.py
        fields = ['id','offense_type_short','offense_type_name']


class OffenseCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Offense Category
    """
    class Meta:
        model = OffenseCategory # use the OffenseCategory model as defined in models.py
        fields = ['id','offense_category_short','offense_category_name']

class NeighbourhoodSerializer(serializers.ModelSerializer):
    """
    Serializer for Neighbourhood
    """
    class Meta:
        model = Neighbourhood  # use the Neighbourhood model as defined in models.py
        fields = '__all__'

class GeolocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Geolocation
    """
    class Meta:
        model = Geolocation # use the Geolocation model as defined in models.py
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location uses a writeable nested serializer - with Geolocation and Neighbourhood nested
    """
    geo = GeolocationSerializer() # use the Geolocation Serializer as defined in serializers.py
    neighbourhood = NeighbourhoodSerializer() # use the Neighbourhood Serializer as defined in serializers.py

    class Meta:
        model = Location # use the Location model as defined in models.py
        fields = ['id','incident_address','district_id','precinct_id','geo','neighbourhood']

    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """

        # from the validated data, get all the geolocation data and remove it from the validated data with pop
        geo_data = validated_data.pop('geo')

        # serialize the geo data
        geo_serializer = GeolocationSerializer(data = geo_data)
        geo_serializer.is_valid()
        geo_instance = geo_serializer.save()

        # from the validated data, get the neighbourhood data and remove it from the validated data with pop
        neighbourhood_data = validated_data.pop('neighbourhood')

        # either get the corresponding neighbourhood instance, or create one.
        # Most often, the neighbourhood will already exist in the database
        neighbourhood, created = Neighbourhood.objects.get_or_create(**neighbourhood_data)

        # create the location object with the relevant data
        location = Location.objects.create(
            incident_address = validated_data['incident_address'],
            district_id = validated_data['district_id'],
            precinct_id = validated_data['precinct_id'],
            neighbourhood = neighbourhood, # with the Neighbourhood object instance
            geo = geo_instance, # with the Geolocation object instance
        )

        return location # custom create function requires location to be returned

class CrimeSerializer(serializers.ModelSerializer):
    """
    Serializer for Crime incident
    """
    location = LocationSerializer()

    class Meta:
        model = Crime # use the Crime model as defined in models.py
        fields = ['id','first_occurrence_date','reported_date','is_crime','is_traffic','location',
                  'victim_count','offense_type','offense_category']


    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        # from the validated data, get all the location data and remove it from the validated data with pop
        location_data = self.validated_data.pop('location')

        # serialize the location data
        location_serializer = LocationSerializer(data = location_data)

        # should the location serializer be valid, save the instance
        if location_serializer.is_valid():
            location_instance = location_serializer.save()
        else:
            raise serializers.ValidationError(location_serializer.errors)

        # create the Crime object instance
        crime = Crime.objects.create(
            first_occurrence_date = validated_data['first_occurrence_date'],
            reported_date = validated_data['reported_date'],
            is_crime = validated_data['is_crime'],
            is_traffic = validated_data['is_traffic'],
            victim_count = validated_data['victim_count'],
            location = location_instance, # use the serialized location instance defined prior
            offense_type = validated_data['offense_type'],
            offense_category = validated_data['offense_category']
        )

        return crime # custom create function requires crime to be returned


