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

    def test_OffenseTypeSerializer(self):
        """Test that the serializer has the right keys."""
        data = self.offense_type
        self.assertEqual(set(data.keys()), set(['offense_type_short','offense_type_name']))

    def test_OffenseTypeSerializer_valid_data(self):
        """Test that the serializer with valid data returns is_valid as true."""
        serializer = OffenseTypeSerializer(data = self.offense_type) # serialize
        self.assertTrue(serializer.is_valid())

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

class LocationSerializerTest(APITestCase):
    """
    Test for the Location Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.location = factory.build(dict, FACTORY_CLASS = LocationFactory)
        self.neighbourhood = NeighbourhoodFactory.create()
        self.geolocation = GeolocationFactory.create()

    def test_LocationSerializer(self):
        "Test that the serializer has the right keys."
        data = self.location
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

        serializer = LocationSerializer(data = data) # serialize the new data
        self.assertTrue(serializer.is_valid())       # assert that the data is valid


class GeolocationSerializerTest(APITestCase):
    """
    Test for the Location Serializer
    """
    def setUp(self):
        """Set up the Test."""
        self.geolocation = factory.build(dict, FACTORY_CLASS = GeolocationFactory)

    def test_GeolocationSerializer(self):
        "Test that the serializer has the right keys."
        data = self.geolocation
        self.assertEqual(set(data.keys()), set(['geo_x','geo_y','geo_lon','geo_lat']))