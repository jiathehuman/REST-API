from incidents.model_factories import *
from incidents.serializers import *
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

class GeolocationTest(APITestCase):

    def setUp(self):
        # Create an offense type using a factory (or manually)
        self.geolocation1 = GeolocationFactory.create(pk = 1)
        self.geolocation2 = GeolocationFactory.create(pk = 2)
        self.geolocation3 = {
            'geo_x': 0.123,
            'geo_y': 123.0,
            'geo_lon': -123.123,
            'geo_lat': -131.12,
        }
        self.good_url = reverse('geolocation', kwargs = {'pk':1})
        self.bad_url = reverse('geolocation', kwargs = {'pk':5}) # bad pk as no pk 5 is created
        self.delete_url = reverse('geolocation',kwargs = {'pk':2})
        self.update_url = reverse('geolocation', kwargs={'pk': 1})


    def test_GeolocationReturnSuccess(self):
        response = self.client.get(self.good_url, format = 'json')
        response.render()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)

    def test_GeolocationDelete(self):
        response = self.client.delete(self.delete_url, format = "json")
        self.assertEqual(response.status_code, 204) # 204 bad content

    def test_GeolocationReturnFail(self):
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)

    def test_GeolocationAPIPut(self):
        # Perform a PUT request to update an existing Geolocation instance with pk=1
        updated_data = {
            'geo_x': 1.234,  # Updated value
            'geo_y': 456.0,  # Updated value
            'geo_lon': -321.123,  # Updated value
            'geo_lat': -141.12,  # Updated value
        }
        response = self.client.put(self.update_url, updated_data, format='json')

        # Check if the status code is 200 OK for a successful update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OffenseTypeListTest(APITestCase):
    def setUp(self):
        """
        Setup method to create some offense types using the factory
        """
        # Create multiple offense types
        self.offense_type_1 = OffenseTypeFactory.create(offense_type_short="ASSAULT", offense_type_name="Assault")
        self.offense_type_2 = OffenseTypeFactory.create(offense_type_short="BURGL", offense_type_name="Burglary")

        # Define the URL for the offense type list view
        self.good_url = reverse('offense_type')
        self.post_url = reverse('offense_type')

    def test_get_offense_type_list(self):
        """
        Test the offense-type list view returns the correct status and data
        """
        response = self.client.get(self.good_url, format="json")

        # Assert the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains a list of offense types
        self.assertEqual(len(response.data), 2)  # Since we created two offense types

    def test_post_offense_type(self):
        """
        Test the POST request to create a new offense type
        """
        # Prepare the data to be sent in the POST request
        new_offense_data = {
            "offense_type_short": "ROBB",
            "offense_type_name": "Robbery"
        }

        # Send the POST request to create a new offense type
        response = self.client.post(self.post_url, new_offense_data, format="json")

        # Assert that the status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the response data contains the fields we sent
        self.assertEqual(response.data['offense_type_short'], new_offense_data['offense_type_short'])
        self.assertEqual(response.data['offense_type_name'], new_offense_data['offense_type_name'])

class NeighbourhoodTest(APITestCase):
    def setUp(self):
        self.neighbourhood = NeighbourhoodFactory.create(pk = 1)
        new_data = {
            'name': "221B Baker Street"
        }
        self.good_url = reverse('neighbourhood',kwargs = {'pk': self.neighbourhood.id})

    def test_get_neighbourhood(self):
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class Api2Test(APITestCase):
    def setUp(self):
        # Create test data
        self.offense_category = OffenseCategoryFactory.create(offense_category_name="Aggravated Assault")
        self.url = reverse('api2', kwargs = {'pk': self.offense_category.id})

    def test_get_hotspots(self):
        """
        Tests if the HotSpots view returns the correct top neighbourhoods.
        """
        response = self.client.get(self.url, format='json')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
