from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from .models import *

from django import forms
from django.forms import modelformset_factory
from .models import Crime, Location
from datetime import date

class CrimeForm(forms.Form):

        first_occurrence_date = forms.DateField(widget=forms.SelectDateWidget)
        reported_date = forms.DateField(widget=forms.SelectDateWidget, initial=date.today)
        is_crime = forms.BooleanField(required=False, initial=False)
        is_traffic = forms.BooleanField(required=False, initial=False)
        victim_count = forms.IntegerField()
        offense_type = forms.ModelChoiceField(queryset = OffenseType.objects.all())
        offense_category = forms.ModelChoiceField(queryset = OffenseCategory.objects.all())

        def clean(self):
            cleaned_data = super().clean()
            # Check if 'is_crime' is not present in cleaned_data (meaning it wasn't ticked)
            if 'is_crime' not in cleaned_data:
                cleaned_data['is_crime'] = False  # Set it to False explicitly
            # Do the same for 'is_traffic' if needed
            if 'is_traffic' not in cleaned_data:
                cleaned_data['is_traffic'] = False  # Set it to False explicitly
            return cleaned_data

        # def clean(self):
        #     cleaned_data = super().clean()

        #     first_occurrence_date = date(
        #             year=int(cleaned_data['first_occurrence_date_year']),
        #             month=int(cleaned_data['first_occurrence_date_month']),
        #             day=int(cleaned_data['first_occurrence_date_day'])
        #         )
        #     reported_date = date(
        #             year=int(cleaned_data['reported_date_year']),
        #             month=int(cleaned_data['reported_date_month']),
        #             day=int(cleaned_data['reported_date_day'])
        #     )

        #     cleaned_data["first_occurrence_date"] = first_occurrence_date
        #     cleaned_data["reported_date"] = reported_date

        #     # Django forms handles Boolean values with a NULL and ON
        #     cleaned_data["is_crime"] = cleaned_data["is_crime"] == "on"
        #     cleaned_data["is_traffic"] = cleaned_data["is_traffic"] == "on"

        #     for field, value in cleaned_data.items():
        #         if value is None:
        #             cleaned_data[field] = ''

        #     return cleaned_data


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['incident_address','district_id','precinct_id','neighbourhood']

class GeolocationForm(forms.ModelForm):
    class Meta:
        model = Geolocation
        fields = '__all__'


