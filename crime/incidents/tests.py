from django.test import TestCase
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# Create your tests here.
class OffenseTypeSerializerTest(APITestCase):
    offenseType = None
    offenseTypeSerializer = None

    # set up called before execution of test method
    def setUp(self):
        self.offenseType = OffenseTypeFactory.create()
        self.offenseTypeSerializer = OffenseTypeSerializer(instance = self.offenseType)

    def tearDown(self):
        Crime.objects.all().delete()
        Location.objects.all().delete()
        Geolocation.objects.all().delete()
        OffenseType.objects.all().delete()
        OffenseCategory.objects.all().delete()
        Neighbourhood.objects.all().delete()
        CrimeFactory.reset_sequence(0)
        LocationFactory.reset_sequence(0)
        GeolocationFactory.reset_sequence(0)
        OffenseTypeFactory.reset_sequence(0)
        OffenseCategoryFactory.reset_sequence(0)
        NeighbourhoodFactory.reset_sequence(0)

    def test_offenseTypeSerializer(self):
        data = self.offenseTypeSerializer.data
        # checking that all keys are present
        self.assertEqual(set(data.keys()),set(['id','offense_type_short','offense_type_name']))

