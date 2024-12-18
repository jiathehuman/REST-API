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


        location = Location.objects.create(
            incident_address = validated_data['incident_address'],
            district_id = validated_data['district_id'],
            precinct_id = validated_data['precinct_id'],
            neighbourhood = Neighbourhood.objects.get(name=validated_data['neighbourhood']),
            geo = geo_instance,
        )

        return location

class CrimeSerializer(serializers.ModelSerializer):
    """
    Serializer for Crime incident
    """
    class Meta:
        model = Crime
        # exclude = ('location',)
        fields = ['id','first_occurrence_date','reported_date','is_crime','is_traffic','location',
                  'victim_count','offense_type','offense_category']

        offense_type = OffenseTypeSerializer()
        offense_category = OffenseCategorySerializer()
        location = LocationSerializer()

    def create(self, validated_data):
        """
        Create and return a `Location` instance, given a validated data
        """
        offense_type_data = validated_data.pop('offense_type')
        offense_category_data = validated_data.pop('offense_category')
        location_data = self.validated_data.pop('location')
        # neighbourhood_data = location_data.pop('neighbourhood')
        # geo_data = location_data.pop('geo')

        # crime = Crime.objects.create(**validated_data)
        # crime.is_valid(raise_exception = True)
        # crime.save()

        location = Location.objects.create(**location_data)
        location.is_valid(raise_exception = True)
        location.save()

        new_crime = Crime(**{
            **validated_data,
            'offense_type' : OffenseType.objects.get(pk = offense_type_data),
            'offense_category': OffenseCategory.objects.get(pk = offense_category_data),
            'location': Location.objects.get(pk = location.data['id'])
        })

        return new_crime




        # location = Location.objects(**location_data)

        # offense_type_data = self.initial_data['offense_type']
        # offense_category_data = self.initial_data['offense_category']
        # location_data = self.initial_data['location']
        # geo_data = location_data['geo']

        # new_geo = GeolocationSerializer(data = geo_data)
        # new_geo.is_valid(raise_exception= True)
        # new_geo.save()

        # location_data['neighbourhood'] = Neighbourhood.objects.get(name__exact = location_data['neighbourhood']).id
        # location_data['geo'] = new_geo.data['id']

        # new_location = LocationSerializer(data = location_data)
        # new_location.is_valid(raise_exception=True)
        # new_location.save()

        # print(new_location)

        # new_crime = Crime(**{
        #     **validated_data,
        #     'offense_type' : OffenseType.objects.get(pk = offense_type_data),
        #     'offense_category': OffenseCategory.objects.get(pk = offense_category_data),
        #     'location': Location.objects.get(pk = new_location.data['id'])
        # })

        # new_crime.save()

        # return new_crime

# class UserSerializer(serializers.ModelSerializer):
#     crimes = serializers.PrimaryKeyRelatedField(many = True, queryset = Crime.objects.all())

#     class Meta:
#         model = User
#         fields = ['id','username','snippets']

