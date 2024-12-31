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
# Classes in the model_factories.py file are PyTest fixtures that are dummy data created for unit tests
# #####

class OffenseTypeFactory(factory.django.DjangoModelFactory):
    """
    Factory for OffenseType model
    """
    offense_type_short = "theft-of-intellectual-property"
    offense_type_name = "Theft of Intellectual Property or Infringement of Copyright"

    class Meta:
        model = OffenseType

class OffenseCategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory for Offense Category model
    """
    offense_category_short = "theft" # eg. theft-from-motor-vehicle
    offense_category_name = "Theft and Stealing" # eg. Theft from Motor Vehicle

    class Meta:
        model = OffenseCategory


class NeighbourhoodFactory(factory.django.DjangoModelFactory):
    """
    Factory for Neighbourhood model
    """
    name = "Derbyshire-Pemberly"

    class Meta:
        model = Neighbourhood

class GeolocationFactory(factory.django.DjangoModelFactory):
    """
    Factory for Geolocatio model that contains the geo-coordinates of the incident
    """
    geo_x = 3.123
    geo_y = 4.132
    geo_lon = 53.338
    geo_lat =  -2.0547

    class Meta:
        model = Geolocation

class LocationFactory(factory.django.DjangoModelFactory):
    """
    Factory for Location model that contains the details of where the incident took place
    """
    incident_address = "1980 Renishaw Hall"
    district_id = 7
    precinct_id = 759
    # geo factory and neighbourhood subfactory are used for the corresponding foreign key relationships
    geo = factory.SubFactory(GeolocationFactory)
    neighbourhood = factory.SubFactory(NeighbourhoodFactory)

    class Meta:
        model = Location

class CrimeFactory(factory.django.DjangoModelFactory):
    """
    Factory for Crime model that contains broad details of the incident
    """
    class Meta:
        model = Crime
    # use fuzzy naive date to get a dummy date
    first_occurrence_date = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2023, 1, 1),datetime.datetime(2023, 2, 1))
    reported_date = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2024, 2, 1),datetime.datetime(2024, 2, 1))
    is_crime = 1
    is_traffic = 1
    victim_count = 1
    location = factory.SubFactory(LocationFactory)
    # offense_type and offense_category subfactory are used for the corresponding foreign key relationships
    offense_type = factory.SubFactory(OffenseTypeFactory)
    offense_category = factory.SubFactory(OffenseCategoryFactory)


