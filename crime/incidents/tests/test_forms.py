from django.test import TestCase
from incidents.model_factories import *
from incidents.forms import *

"""
Test file for Form tests
"""

class TestCrimeForm(TestCase):
    """
    Test for the Crime Form
    """
    def setUp(self):
        "Set up the Test"
        self.offense_category = OffenseCategoryFactory.create() # create factory for offense_category
        self.offense_type = OffenseTypeFactory.create() # create factory for offense_type
        self.location = LocationFactory.create() # create factory for location
        self.crime = factory.build(dict,FACTORY_CLASS = CrimeFactory)

    def test_crimeform_is_valid(self):
        """Test that the Form is valid if given valid data"""

        # define valid data
        form_data = {
            "first_occurrence_date": self.crime["first_occurrence_date"],
            "reported_date": self.crime["reported_date"],
            "is_crime": self.crime["is_crime"],
            "victim_count": self.crime["victim_count"],
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        # feed the data into the form
        form = CrimeForm(data=form_data)

        # assert that form is valid
        self.assertTrue(form.is_valid())

    def test_crimeform_invalid_date(self):
        """Test that form is invalid if the reported date is before the occurrence date."""
        # define invalid data (reported date is before occurrence date)
        form_data = {
            "first_occurrence_date": datetime.datetime(2025, 1, 1),
            "reported_date": datetime.datetime(2023, 1, 1),
            "is_crime": self.crime["is_crime"],
            "victim_count": self.crime["victim_count"],
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data) # feed valid data into form
        self.assertFalse(form.is_valid()) # assert that form is invalid
        self.assertEqual(len(form.errors), 1) # assert that the form has 1 error

    def test_crimeform_invalid_victim_count(self):
        """Test that form is invalid if the victim count is negative."""
        form_data = {
            "first_occurrence_date": self.crime["first_occurrence_date"],
            "reported_date": self.crime["reported_date"],
            "is_crime": self.crime["is_crime"],
            "victim_count": -1,
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data) # feed invalid data into form
        self.assertFalse(form.is_valid()) # assert that form is invalid
        self.assertEqual(len(form.errors), 1) # assert that the form has 1 error

    def test_crimeform_handles_multiple_invalid(self):
        """Test that the form catches multiple errors."""
        form_data = {
            "first_occurrence_date": datetime.datetime(2025, 1, 1), # Error 1: Reported date < Occurrence date
            "reported_date": datetime.datetime(2023, 1, 1),
            "is_crime": self.crime["is_crime"],
            "victim_count": -1,                                     # Error 2: Victim count is negative
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data) # feed invalid data into fomr
        self.assertFalse(form.is_valid()) # assert that form is invalid
        self.assertEqual(len(form.errors), 2) # assert that the form has 1 error

class TestOffenseCategoryForm(TestCase):
    """
    Test for the Offense Category Form
    """
    def setUp(self):
        """Set up the test."""
        self.offense_category = OffenseCategoryFactory.create() # create factory

    def test_offenseCategoryform_is_valid(self):
        """Test that the form is valid if given correct data"""

        # correct data
        form_data = {
            "offense_category": self.offense_category.pk
        }

        form = OffenseCategoryForm(data = form_data) # feed data into form
        self.assertTrue(form.is_valid())            # assert that form is valid

    def test_offenseCategoryform_is_invalid(self):
        """Test that the form is invalid if given wrong data."""
        form_data = {
            "offense_category": "Invalid string" # invalid data as offense category should be a pk
        }
        form = OffenseCategoryForm(data = form_data) # feed data into form
        self.assertFalse(form.is_valid())           # assert that form is not valid

class TestGeolocationForm(TestCase):
    """
        Test for the Geolocation Form
    """
    def setUp(self):
        self.geolocation = GeolocationFactory.create() # create geolocation factory

    def test_is_valid(self):
        """Test that Form is valid if given correct data."""
        # correct data
        form_data = {
            "geo_x" : self.geolocation.geo_x,
            "geo_y" : self.geolocation.geo_y,
            "geo_lon" : self.geolocation.geo_lon,
            "geo_lat" : self.geolocation.geo_lat
        }
        form = GeolocationForm(data=form_data) # feed data into form
        self.assertTrue(form.is_valid())      # assert that form is valid

    def test_is_invalid(self):
        """Test that Form is invalid if given data of wrong type"""
        form_data = {
            # data for geocoordinates should be float, not string
            "geo_x" : "abc",
            "geo_y" : "abc",
            "geo_lon" : "abc",
            "geo_lat" : "abc"
        }

        form = OffenseCategoryForm(data = form_data) # feed data into form
        self.assertFalse(form.is_valid()) # assert that form is invalid


class TestLocationForm(TestCase):
    """
    Test for the Locatin Form
    """
    def setUp(self):
        """Set up the test"""
        self.geolocation = GeolocationFactory.create()
        self.neighbourhood = NeighbourhoodFactory.create()
        self.location = factory.build(dict,FACTORY_CLASS = LocationFactory)

    def test_locationform_is_valid(self):
        """Test that form is valid when given correct data"""
        # valid data
        form_data = {
            "incident_address" : self.location["incident_address"],
            "district_id" : self.location["district_id"],
            "precinct_id" : self.location["precinct_id"],
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data) # feed data into form
        self.assertTrue(form.is_valid()) # assert that form is valid

    def test_locationform_invalid_district(self):
        """Test that form is invalid when a negative district id"""
        form_data = {
            "incident_address" : self.location["incident_address"],
            "district_id" : -1,
            "precinct_id" : self.location["precinct_id"],
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data) # feed data into form
        self.assertFalse(form.is_valid()) # assert that form is invalid

    def test_locationform_invalid_precinct(self):
        """Test that form is invalid when a negative precinct id"""
        form_data = {
            "incident_address" : self.location["incident_address"],
            "district_id" : self.location["district_id"],
            "precinct_id" : -1,
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data) # feed data into form
        self.assertFalse(form.is_valid()) # assert that form is invalid




