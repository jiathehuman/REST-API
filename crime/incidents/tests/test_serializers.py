from incidents.model_factories import *
from incidents.serializers import *
from rest_framework.test import APITestCase

"""
Test file for Serializers
"""

class OffenseTypeSerializerTest(APITestCase):
    """
    Test for the Offense Type Serializer
    """
    def setUp(self):
        """Set up the Test."""
        # Set up the offense type instance with factory boy
        self.offense_type = factory.build(dict, FACTORY_CLASS = OffenseTypeFactory)
        self.offense_type_serializer = OffenseTypeSerializer(data = self.offense_type)
        self.offense_type_serializer.is_valid()
        self.data = self.offense_type_serializer.data

    def test_OffenseTypeSerializer(self):
        """Test that the serializer has the right keys."""
        # data = self.offense_type
        self.assertEqual(set(self.data.keys()), set(['offense_type_short','offense_type_name']))

    def test_OffenseTypeSerializer_valid_data(self):
        """Test that the serializer with valid data returns is_valid as true."""
        # serializer = OffenseTypeSerializer(data = self.offense_type) # serialize
        self.assertTrue(self.offense_type_serializer.is_valid())

    def test_OffenseTypeSerializer_invalid_data(self):
        """Test that the serializer with invalid data returns is_valid as true."""
        invalid_data = {
            "offense_type_short": "", # invalid missing data
            "offense_type_name": "Hacking into government database"
        }
        serializer = OffenseTypeSerializer(data = invalid_data) # serialize
        self.assertFalse(serializer.is_valid()) # check that is_valid() returns false
        self.assertIn("offense_type_short", serializer.errors) # check that the errors contain the error field

    def test_OffenseTypeSerializer_saves(self):
        """Test that the serializer saves valid data."""

        # define new data to save
        new_data = {
            "offense_type_short": "hack",
            "offense_type_name": "Hacking into commercial database"
        }
        serializer = OffenseTypeSerializer(data=new_data) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance

        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.offense_type_short, "hack")
        self.assertEqual(saved_instance.offense_type_name, "Hacking into commercial database")

class OffenseCategorySerializerTest(APITestCase):
    """
    Test for the Offense Type Serializer
    """
    def setUp(self):
        """Set up the Test."""
        # Set up the offense type instance with factory boy
        self.offense_category = factory.build(dict, FACTORY_CLASS = OffenseCategoryFactory)
        self.offense_category_serializer = OffenseCategorySerializer(data = self.offense_category)
        self.offense_category_serializer.is_valid()
        self.data = self.offense_category_serializer.data

    def test_OffenseCategorySerializer(self):
        """Test that the serializer has the right keys."""
        # data = self.offense_type
        self.assertEqual(set(self.data.keys()), set(['offense_category_short','offense_category_name']))

    def test_OffenseCategorySerializer_valid_data(self):
        """Test that the serializer with valid data returns is_valid as true."""
        # serializer = OffenseTypeSerializer(data = self.offense_type) # serialize
        self.assertTrue(self.offense_category_serializer.is_valid())

    def test_OffenseCategorySerializer_invalid_data(self):
        """Test that the serializer with invalid data returns is_valid as true."""
        invalid_data = {
            "offense_category_short": "", # invalid missing data
            "offense_category_name": "Burglary"
        }
        serializer = OffenseCategorySerializer(data = invalid_data) # serialize
        self.assertFalse(serializer.is_valid()) # check that is_valid() returns false
        self.assertIn("offense_category_short", serializer.errors) # check that the errors contain the error field

    def test_OffenseCategorySerializer_saves(self):
        """Test that the serializer saves valid data."""

        # define new data to save
        new_data = {
            "offense_category_short": "burg",
            "offense_category_name": "Burglary"
        }
        serializer = OffenseCategorySerializer(data=new_data) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance
        else:
            raise serializers.ValidationError(f"OffenseCategorySerializerTest.OffenseCategorySerializer_saves: {serializer.errors}")

        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.offense_category_short, 'burg')
        self.assertEqual(saved_instance.offense_category_name, 'Burglary')


class LocationSerializerTest(APITestCase):
    """
    Test for the Location Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.location = factory.build(dict, FACTORY_CLASS = LocationFactory)
        self.location_serializer = LocationSerializer(data = self.location)
        self.location_serializer.is_valid()
        self.neighbourhood = NeighbourhoodFactory.create()
        self.geolocation = GeolocationFactory.create()
        self.valid_data = {'incident_address': '211B Baker Street',
                'district_id': 7,
                'precinct_id': 759,
                'geo': {
                    'geo_x' : self.geolocation.geo_x,
                    'geo_y' : self.geolocation.geo_y,
                    'geo_lat': self.geolocation.geo_lat,
                    'geo_lon': self.geolocation.geo_lon
                },
                'neighbourhood': {"name": self.neighbourhood.name
            }}

    def test_LocationSerializer(self):
        "Test that the serializer has the right keys."
        data = self.location_serializer.data
        # assert that all the keys are defined correctly
        self.assertEqual(set(data.keys()), set(['incident_address','district_id','precinct_id','geo','neighbourhood']))

    def test_LocationSerializer_valid_data(self):
        """Test the serializer with valid data."""
        # define new data
        data = {'incident_address': '211B Baker Street',
                'district_id': 7,
                'precinct_id': 759,
                'geo': {
                    'geo_x' : self.geolocation.geo_x,
                    'geo_y' : self.geolocation.geo_y,
                    'geo_lat': self.geolocation.geo_lat,
                    'geo_lon': self.geolocation.geo_lon
                },
                'neighbourhood': {"name": self.neighbourhood.name
            }}

        serializer = LocationSerializer(data = self.valid_data) # serialize the new data
        self.assertTrue(serializer.is_valid())       # assert that the data is valid

    def test_LocationSerializer_saves(self):
        """Test that the serializer saves valid data."""

        serializer = LocationSerializer(data=self.valid_data) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance
        else:
            raise serializers.ValidationError(serializer.errors)

        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.incident_address, self.valid_data['incident_address'])

class GeolocationSerializerTest(APITestCase):
    """
    Test for the Location Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.geolocation = factory.build(dict, FACTORY_CLASS = GeolocationFactory)
        self.geolocation2 = factory.build(dict, FACTORY_CLASS = GeolocationFactory)
        self.geolocation_serializer = GeolocationSerializer(data = self.geolocation)
        self.geolocation_serializer.is_valid()
        self.data = self.geolocation_serializer.data

    def test_GeolocationSerializer(self):
        "Test that the serializer has the right keys."
        self.assertEqual(set(self.data.keys()), set(['geo_x','geo_y','geo_lon','geo_lat']))

    def test_GeolocationSerializer_saves(self):
        """Test that the serializer saves valid data."""

        serializer = GeolocationSerializer(data=self.geolocation2) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance
        else:
            raise serializers.ValidationError(serializer.errors)

        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.geo_x, self.geolocation2['geo_x'])


class NeighbourhoodSerializerTest(APITestCase):
    """
    Test for the Neighbourhood Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.neighbourhood = factory.build(dict, FACTORY_CLASS = NeighbourhoodFactory)
        self.neighbourhood2 = factory.build(dict, FACTORY_CLASS = NeighbourhoodFactory)
        self.neighbourhood_serializer = NeighbourhoodSerializer(data = self.neighbourhood)
        self.neighbourhood_serializer.is_valid()
        self.data = self.neighbourhood_serializer.data

    def test_NeighbourhoodSerializer(self):
        "Test that the serializer has the right keys."
        self.assertEqual(set(self.data.keys()), set(['name']))

    def test_NeighbourhoodSerializer_correct_data(self):
        "Test that the serializer has the right data."
        self.assertEqual(self.data['name'], self.neighbourhood['name'])

    def test_NeighbourhoodSerializer_saves(self):
        """Test that the serializer saves valid data."""

        serializer = NeighbourhoodSerializer(data=self.neighbourhood2) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance
        else:
            raise serializers.ValidationError(serializer.errors)

        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.name, self.neighbourhood2['name'])

class CrimeSerializerTest(APITestCase):
    """
    Test for the Crime Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.crime = factory.build(dict, FACTORY_CLASS = CrimeFactory)
        self.crime2 = factory.build(dict, FACTORY_CLASS = CrimeFactory)
        self.geo = GeolocationFactory.create(pk = 1)
        self.neighbourhood = NeighbourhoodFactory.create(pk = 1)
        self.offense_type = OffenseTypeFactory.create(pk = 1)
        self.offense_category = OffenseCategoryFactory.create(pk = 1)
        self.crime_serializer = CrimeSerializer(data = self.crime)
        self.crime_serializer.is_valid()
        self.data = self.crime_serializer.data

    def test_CrimeSerializer(self):
        "Test that the serializer has the right keys."
        self.assertEqual(set(self.data.keys()), set(['first_occurrence_date','reported_date','is_crime','is_traffic','location',
                  'victim_count','offense_type','offense_category']))

    def test_CrimeSerializer_correct_data(self):
        "Test that the serializer has the right data"
        self.assertEqual(self.data['first_occurrence_date'], self.crime['first_occurrence_date'])

    def test_CrimeSerializer_saves(self):
        """Test that the serializer saves valid data."""
        valid_data = {
        "id": 20014,
        "first_occurrence_date": "2025-01-01T00:00:00",
        "reported_date": "2026-01-01T00:00:00",
        "is_crime": True,
        "is_traffic": False,
        "location": {
            "id": 20014,
            "incident_address": "211B Baker Street",
            "district_id": 2,
            "precinct_id": 3,
            "geo": {
                "id": 1,
                "geo_x": 1.0,
                "geo_y": -3.0,
                "geo_lon": 4.0,
                "geo_lat": -3.0
            },
            "neighbourhood": {
                "id": 1,
                "name": "west-highland"
            }
        },
        "victim_count": 5,
        "offense_type": 1,
        "offense_category": 1
        }
        serializer = CrimeSerializer(data=valid_data) # serialize the new data
        if serializer.is_valid():                         # call is valid before save()
            saved_instance = serializer.save()            # save the instance
        else:
            raise serializers.ValidationError(serializer.errors)

        self.assertTrue(serializer.is_valid())
        # test that the saved serializer's data is the same as given
        self.assertEqual(saved_instance.victim_count, valid_data["victim_count"])