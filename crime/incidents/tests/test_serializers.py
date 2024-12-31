from django.test import TestCase
from incidents.model_factories import *
from incidents.serializers import *
from rest_framework.test import APITestCase


class OffenseTypeSerializerTest(APITestCase):
    def setUp(self):
        self.offense_type = factory.build(dict, FACTORY_CLASS = OffenseTypeFactory)

    def tearDown(self):
        OffenseTypeFactory.reset_sequence(0)

    def test_OffenseTypeSerializer(self):
        data = self.offense_type
        self.assertEqual(set(data.keys()), set(['offense_type_short','offense_type_name']))

    def test_OffenseTypeSerializer_valid_data(self):
        """Test the serializer with valid data."""
        serializer = OffenseTypeSerializer(data = self.offense_type)
        self.assertTrue(serializer.is_valid())

    def test_OffenseTypeSerializer_invalid_data(self):
        invalid_data = {
            "offense_type_short": "",
            "offense_type_name": "Burglary"
        }
        serializer = OffenseTypeSerializer(data = invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("offense_type_short", serializer.errors)

    def test_OffenseTypeSerializer_saves(self):
        new_data = {
            "offense_type_short": "hack",
            "offense_type_name": "Hacking into commercial database"
        }
        serializer = OffenseTypeSerializer(data=new_data)
        if serializer.is_valid():
            saved_instance = serializer.save()
        self.assertEqual(saved_instance.offense_type_short, "hack")
        self.assertEqual(saved_instance.offense_type_name, "Hacking into commercial database")

class LocationSerializerTest(APITestCase):
    def setUp(self):
        self.location = factory.build(dict, FACTORY_CLASS = LocationFactory)
        self.neighbourhood = NeighbourhoodFactory.create()
        self.geolocation = GeolocationFactory.create()

    def test_LocationSerializer(self):
        data = self.location
        self.assertEqual(set(data.keys()), set(['incident_address','district_id','precinct_id','geo','neighbourhood']))

    def test_LocationSerializer_valid_data(self):
        """Test the serializer with valid data."""
        data = {'incident_address': '1980 Renishaw Hall',
                'district_id': 7,
                'precinct_id': 759,
                'geo': {
                    'geo_x' : self.geolocation.geo_x,
                    'geo_y' : self.geolocation.geo_y,
                    'geo_lat': self.geolocation.geo_lat,
                    'geo_lon': self.geolocation.geo_lon
                },
                'neighbourhood': {"name": self.neighbourhood.name}}

        serializer = LocationSerializer(data = data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())

class GeolocationSerializerTest(APITestCase):
    def setUp(self):
        self.geolocation = factory.build(dict, FACTORY_CLASS = GeolocationFactory)

    def tearDown(self):
        GeolocationFactory.reset_sequence(0)

    def test_GeolocationSerializer(self):
        data = self.geolocation
        self.assertEqual(set(data.keys()), set(['geo_x','geo_y','geo_lon','geo_lat']))