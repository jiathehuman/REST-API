from django.test import TestCase
from rest_framework.test import APITestCase
from datetime import date, timedelta

from .forms import *
from .model_factories import *
from .serializers import *

# Create your tests here.
class OffenseTypeSerializerTest(APITestCase):
    """
    Test to assess the function of the Offense Type Serializer
    """
    offenseType = None
    offenseTypeSerializer = None

    # set up called before execution of test method
    def setUp(self):
        """
        Set up the variables for the test
        """
        self.offenseType = OffenseTypeFactory.create()
        self.offenseTypeSerializer = OffenseTypeSerializer(instance = self.offenseType)

    def tearDown(self):
        """
        Remove the testing data upon finishing execution
        """
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
        """
        Test that all the keys are present
        """
        data = self.offenseTypeSerializer.data
        # checking that all keys are present
        self.assertEqual(set(data.keys()),set(['id','offense_type_short','offense_type_name']))

    def test_offenseTypeSerializerContainsRightData(self):
        """
        Test correctness of the data
        """
        data = self.offenseTypeSerializer.data
        self.assertEqual(data['offense_type_short'],'theft-of-intellectual-property')

# class CrimeFormTests(TestCase):
#     def setUp(self):
#         """
#         Set up the variables for the test
#         """
#         self.offenseType = OffenseTypeFactory.create()
#         self.offenseCategory = OffenseCategoryFactory.create()

#     def tearDown(self):
#         """
#         Remove the testing data upon finishing execution
#         """
#         Crime.objects.all().delete()
#         Location.objects.all().delete()
#         Geolocation.objects.all().delete()
#         OffenseType.objects.all().delete()
#         OffenseCategory.objects.all().delete()
#         Neighbourhood.objects.all().delete()
#         CrimeFactory.reset_sequence(0)
#         LocationFactory.reset_sequence(0)
#         GeolocationFactory.reset_sequence(0)
#         OffenseTypeFactory.reset_sequence(0)
#         OffenseCategoryFactory.reset_sequence(0)
#         NeighbourhoodFactory.reset_sequence(0)

#     def test_valid_form(self):
#         """
#         Test if the form is valid
#         """
#         form_data = {
#             "first_occurrence_date": date.today(),
#             "reported_date": date.today(),
#             "is_crime": True,
#             "is_traffic": False,
#             "victim_count": 1,
#             "offense_type": self.offenseType.id,
#             "offense_category": self.offenseCategory.id,
#         }
#         form = CrimeForm(data = form_data)
#         self.assertTrue(form.is_valid())