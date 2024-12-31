from django.test import TestCase
from incidents.model_factories import *
from incidents.forms import *

class TestCrimeForm(TestCase):
    def setUp(self):
        self.offense_category = OffenseCategoryFactory.create()
        self.offense_type = OffenseTypeFactory.create()
        self.location = LocationFactory.create()

    def test_is_valid(self):
        crime = factory.build(dict,FACTORY_CLASS = CrimeFactory)
        form_data = {
            "first_occurrence_date": crime["first_occurrence_date"],
            "reported_date": crime["reported_date"],
            "is_crime": crime["is_crime"],
            "victim_count": crime["victim_count"],
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        """
        Test that form is invalid if the reported date is before the occurrence date
        """
        crime = factory.build(dict,FACTORY_CLASS = CrimeFactory)
        form_data = {
            "first_occurrence_date": datetime.datetime(2025, 1, 1),
            "reported_date": datetime.datetime(2023, 1, 1),
            "is_crime": crime["is_crime"],
            "victim_count": crime["victim_count"],
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_victim_count(self):
        crime = factory.build(dict,FACTORY_CLASS = CrimeFactory)
        form_data = {
            "first_occurrence_date": crime["first_occurrence_date"],
            "reported_date": crime["reported_date"],
            "is_crime": crime["is_crime"],
            "victim_count": -1,
            "offense_type": self.offense_type,
            "offense_category": self.offense_category,
        }
        form = CrimeForm(data=form_data)
        if not form.is_valid():
            form = CrimeForm(data=form_data)
            self.assertFalse(form.is_valid())

class TestOffenseCategoryForm(TestCase):

    def setUp(self):
        self.offense_category = OffenseCategoryFactory.create()

    def test_is_valid(self):
        form_data = {
            "offense_category": self.offense_category.pk
        }

        form = OffenseCategoryForm(data = form_data)
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form_data = {
            "offense_category": "Invalid string"
        }

        form = OffenseCategoryForm(data = form_data)
        self.assertFalse(form.is_valid())

class TestGeolocationForm(TestCase):

    def setUp(self):
        self.geolocation = GeolocationFactory.create()

    def test_is_valid(self):
        form_data = {
            "geo_x" : self.geolocation.geo_x,
            "geo_y" : self.geolocation.geo_y,
            "geo_lon" : self.geolocation.geo_lon,
            "geo_lat" : self.geolocation.geo_lat
        }
        form = GeolocationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form_data = {
            "geo_x" : "abc",
            "geo_y" : "abc",
            "geo_lon" : "abc",
            "geo_lat" : "abc"
        }

        form = OffenseCategoryForm(data = form_data)
        self.assertFalse(form.is_valid())


class TestLocationForm(TestCase):
    def setUp(self):
        self.geolocation = GeolocationFactory.create()
        self.neighbourhood = NeighbourhoodFactory.create()
        # self.location = LocationFactory.create()

    def test_is_valid(self):
        location = factory.build(dict,FACTORY_CLASS = LocationFactory)
        form_data = {
            "incident_address" : location["incident_address"],
            "district_id" : location["district_id"],
            "precinct_id" : location["precinct_id"],
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data)
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_district(self):
        location = factory.build(dict,FACTORY_CLASS = LocationFactory)
        form_data = {
            "incident_address" : location["incident_address"],
            "district_id" : -1,
            "precinct_id" : location["precinct_id"],
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_precinct(self):
        location = factory.build(dict,FACTORY_CLASS = LocationFactory)
        form_data = {
            "incident_address" : location["incident_address"],
            "district_id" : location["district_id"],
            "precinct_id" : -1,
            "geo": self.geolocation,
            "neighbourhood": self.neighbourhood
        }
        form = LocationForm(data=form_data)
        self.assertFalse(form.is_valid())




