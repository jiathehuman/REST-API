from incidents.model_factories import *
from incidents.serializers import *
from incidents.forms import *
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

"""
Test file for API tests
"""
class HotspotTest(APITestCase):
    """
    Test for the Hotspot endpoint.
    """
    def setUp(self):
        """Set up test"""
        # Create test data
        self.offense_category = OffenseCategoryFactory.create(offense_category_name="Aggravated Assault")
        self.url = reverse('api2', kwargs = {'pk': self.offense_category.id})

    def test_get_hotspots(self):
        """
        Tests if the HotSpots view returns the correct top neighbourhoods.
        """
        response = self.client.get(self.url, format='json')

        # assert that response status code is 200 ok
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GeolocationDetailTest(APITestCase):
    """
    Test for the Geolocation endpoint
    """
    def setUp(self):
        # Create an offense type using a factory
        self.geolocation1 = GeolocationFactory.create(pk = 1)
        self.geolocation2 = GeolocationFactory.create(pk = 2)

        # Define URLs
        self.good_url = reverse('geolocation', kwargs = {'pk':1})
        self.bad_url = reverse('geolocation', kwargs = {'pk':5}) # bad pk as no pk 5 is created
        self.delete_url = reverse('geolocation',kwargs = {'pk':2})
        self.update_url = reverse('geolocation', kwargs={'pk': 1})


    def test_geolocation_get(self):
        """Test that a valid url pattern return HTTP status of 200"""
        response = self.client.get(self.good_url, format = 'json') # get the pk 1
        response.render() # render the response such that we can test for the pk
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200) # 200 ok
        self.assertEqual(data['id'], 1) # assert that pk retrieved is the pk we gave

    def test_geolocation_delete(self):
        """Test that a call to Delete is successful"""
        response = self.client.delete(self.delete_url, format = "json")
        self.assertEqual(response.status_code, 204) # 204 no content there, delete successful

    def test_geolocation_pk_fail(self):
        """Test that a bad url pattern with an invalid pk return HTTP status of 404"""
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)

    def test_geolocation_put(self):
        """Test that a call to PUT or UPDATE is successful"""
        # Perform a PUT request to update an existing Geolocation instance with pk=1
        # Data to update
        updated_data = {
            'geo_x': 1.234,
            'geo_y': 456.0,
            'geo_lon': -321.123,
            'geo_lat': -141.12,
        }
        # Call PUT on API
        response = self.client.put(self.update_url, updated_data, format='json')

        # Check if the status code is 200 OK for a successful update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OffenseTypeListTest(APITestCase):
    """
    Test for the Offense Type endpoint.
    """
    def setUp(self):
        """
        Set up the Test.
        """
        # Create multiple offense types
        self.offense_type_1 = OffenseTypeFactory.create(offense_type_short="Hack1", offense_type_name="Hack into a commercial server")
        self.offense_type_2 = OffenseTypeFactory.create(offense_type_short="Hack2", offense_type_name="Hack at a tree")

        # urls for the list views
        self.good_url = reverse('offense_type')
        self.post_url = reverse('offense_type')

    def test_get_offense_type_list(self):
        """Test that the view returns the correct status and data"""
        response = self.client.get(self.good_url, format="json")

        # assert the response status is 200 ok
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert the response data contains two offenses
        self.assertEqual(len(response.data), 2)  # Since we created two offense types

    def test_post_offense_type(self):
        """ Test the POST request to create a new offense type"""

        # data to be sent
        new_offense_data = {
            "offense_type_short": "Walk-on-grass",
            "offense_type_name": "Walking on Grass of Private Property"
        }

        # send post to create new offense type
        response = self.client.post(self.post_url, new_offense_data, format="json")

        # assert that satus code is 201 created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert that the fields match
        self.assertEqual(response.data['offense_type_short'], new_offense_data['offense_type_short'])
        self.assertEqual(response.data['offense_type_name'], new_offense_data['offense_type_name'])

class NeighbourhoodListTest(APITestCase):
    """
    Test for the Neighbourhood endpoint.
    """
    def setUp(self):
        """Set up the Test."""
        self.neighbourhood = NeighbourhoodFactory.create(pk = 1)
        self.neighbourhood2 = NeighbourhoodFactory.create(pk = 2)
        self.good_url = reverse('neighbourhood',kwargs = {'pk': self.neighbourhood.id})
        self.delete_url = reverse('neighbourhood',kwargs = {'pk':self.neighbourhood2.id})

    def test_get_neighbourhood(self):
        """
        Test that getting the neighbourhood by pk is successful
        """
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # assert that response.status_code is 200 ok

    def test_put_neighbourhood(self):
        """Test that getting the neighbourhood by pk is successful"""
        updated_data = {
            'name': '211B Baker Street'
        }
        # Call PUT on API
        response = self.client.put(self.good_url, updated_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # assert that response.status_code is 200 ok

    def test_delete_neighbourhood(self):
        """Test that deleting the neighbourhood is successful"""
        response = self.client.delete(self.delete_url, format = "json")
        self.assertEqual(response.status_code, 204) # 204 no content there, delete successful



