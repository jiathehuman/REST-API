import factory
from random import randint
from random import choice
from django.test import TestCase
from django.conf import Settings
from django.core.files import File
from factory import fuzzy
import datetime

from .models import *

######
# Classes in the model_factories.py file are PyTest fixtures that are dummy data for testing
# #####

class OffenseTypeFactory(factory.django.DjangoModelFactory):
    offense_type_short = "theft-of-intellectual-property"
    offense_type_name = "Theft of Intellectual Property or Infringement of Copyright"

    class Meta:
        model = OffenseType

class OffenseCategoryFactory(factory.django.DjangoModelFactory):
    offense_category_short = "theft" # eg. theft-from-motor-vehicle
    offense_category_name = "Theft and Stealing" # eg. Theft from Motor Vehicle


class NeighbourhoodFactory(factory.django.DjangoModelFactory):
    name = "Derbyshire-Pemberly"

class GeolocationFactory(factory.django.DjangoModelFactory):
    """
    Model for Geolocation that contains the geo-coordinates of the incident
    """
    geo_x = 3.123
    geo_y = 4.132
    geo_lon = 53.338
    geo_lat =  -2.0547

class LocationFactory(factory.django.DjangoModelFactory):
    """
    Model for Location that contains the details of where the incident took place
    """
    incident_address = "1980 Renishaw Hall"
    district_id = 7
    precinct_id = 759
    geo = factory.SubFactory(GeolocationFactory)
    neighbourhood = factory.SubFactory(NeighbourhoodFactory)

class CrimeFactory(factory.django.DjangoModelFactory):
    """
    Model for Crime that contains broad details of the incident
    """
    first_occurrence_date = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2023, 1, 1))
    reported_date = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2023, 1, 1))
    is_crime = 1
    is_traffic = 1
    victim_count = 1
    offense_type = factory.SubFactory(OffenseTypeFactory)
    offense_category = factory.SubFactory(OffenseCategoryFactory)
