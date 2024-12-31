from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from .models import *

from django import forms
from django.forms import modelformset_factory
from .models import Crime, Location
from datetime import date


class CrimeForm(forms.Form):
    """
    Form to create a new Crime
    """
    error_css_class = "error"
    required_css_class = "required"

    # define the fields for the Form
    first_occurrence_date = forms.DateField(widget=forms.SelectDateWidget)
    reported_date = forms.DateField(widget=forms.SelectDateWidget, initial=date.today)
    is_crime = forms.BooleanField(required=False, initial=False)
    is_traffic = forms.BooleanField(required=False, initial=False)
    victim_count = forms.IntegerField()
    offense_type = forms.ModelChoiceField(queryset = OffenseType.objects.all())
    offense_category = forms.ModelChoiceField(queryset = OffenseCategory.objects.all())

    # Overwrite the clean function for the form for custom validation
    def clean(self):
        # get all the data that are passed into the form and cleaned
        cleaned_data = super(CrimeForm, self).clean()

        # get the data in the date fields
        first_occurrence = cleaned_data.get("first_occurrence_date")
        reported_date = cleaned_data.get("reported_date")

        # get the fields that should not be negative
        victim_count = cleaned_data.get("victim_count")

        # dictionary for errors
        errors = {}

        # checking date
        if first_occurrence and reported_date and first_occurrence > reported_date:
            errors['first_occurrence_date'] = "First occurrence must be before reported date."

        # check that victim count is not negative, append the error to the errors dict
        if victim_count < 0:
            errors['victim_count'] = "Victim count cannot be a negative number."

        # if there are any errors, raise it with ValidationError
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class LocationForm(forms.ModelForm):
    """
    Form to create a new Location
    """
    class Meta:
        model = Location
        # only get the fields that we need
        fields = ['incident_address','district_id','precinct_id','neighbourhood']

    def clean(self):
        cleaned_data = super(LocationForm, self).clean()
        district_id = cleaned_data.get("district_id")
        precinct_id = cleaned_data.get("precinct_id")

        errors = {}

        # check that district_id is not negative, append the error to the errors dict
        if district_id < 0:
            errors['district_id'] = "Victim count cannot be a negative number."

        # check that precinct_id is not negative, append the error to the errors dict
        if precinct_id < 0:
            errors['precinct_id'] = "Victim count cannot be a negative number."

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

class GeolocationForm(forms.ModelForm):
    """
    Form to create a new Geolocation
    """
    class Meta:
        model = Geolocation
        # get all the fields
        fields = '__all__'

class OffenseCategoryForm(forms.Form):
    """
    Form to create a new Geolocation
    """
    offense_category = forms.ModelChoiceField(queryset = OffenseCategory.objects.all())