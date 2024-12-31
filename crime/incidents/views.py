from rest_framework import mixins, generics
from django.db.models import Count, F, Q
from datetime import date, datetime
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
import math

from .forms import *
from .models import *
from .serializers import *


# Reference: https://www.django-rest-framework.org/tutorial/3-class-based-views/
# Reference for aggregation: https://docs.djangoproject.com/en/5.1/topics/db/aggregation/

def index(request):
    """
    Index page
    """
    # If the request method is GET, render the Form and initialise values.
    if request.method == 'GET':
        category_form = OffenseCategoryForm()
        neighbourhood_ids = list(Neighbourhood.objects.all().values_list('id', flat=True))
        geolocation_ids  = list(Geolocation.objects.all().values_list('id', flat=True))
        range_neighbourhood_values = range(neighbourhood_ids[0],neighbourhood_ids[-1]) # for neighbourhood detail view
        range_geolocation_values = range(geolocation_ids[0],geolocation_ids[-1]) # for geolocation detail view
        # render the index page with the form and the initialised values
        return render(request, 'incidents/index.html',{
            'form': category_form,
            'n_range': range_neighbourhood_values,
            'g_range': range_geolocation_values
        })
    # If the request is POST, get the Form details.
    elif request.method == 'POST':
        category_form = OffenseCategoryForm(request.POST)

        # Validate the form
        if category_form.is_valid():
            # If the form is valid, extract the offense category short from the form data
            offense_category = category_form.cleaned_data.get('offense_category')

            # Redirect to the HotSpots page with the offense_category_short as a query parameter
            return redirect('api2', pk = offense_category.id)

        else:
            # If the form is invalid, render the form again with errors
            return render(request, 'incidents/index.html', {'form': category_form,
                                                            'range': range_neighbourhood_values,
                                                            'g_range': range_geolocation_values})


def NewCrime(request):
    """"
    GET returns list of 5 most recent crimes.
    POST creates a new crime. This creates and updates across all 6 tables.
    Validations is done through serializers
    """

    # If the method is GET,
    if request.method == 'GET':
        # instantiate the three Form objects
        crime_form = CrimeForm()
        location_form = LocationForm()
        geolocation_form = GeolocationForm()

        # render the page with the Forms
        return render(request,'incidents/new_crime.html',{
            'crime_form' : crime_form,
            'location_form' : location_form,
            'geolocation_form': geolocation_form
        })

    # If the method is POST, aka user submit the form:
    elif request.method == 'POST':
        crime_form = CrimeForm(request.POST)
        location_form = LocationForm(request.POST)
        geolocation_form = GeolocationForm(request.POST)

        data_dict = {} # initialise a dictionary to store the data from the form

        # validate the data in the form
        if crime_form.is_valid() and location_form.is_valid() and geolocation_form.is_valid():

            # for each key value pair inside the items in POST
            for key, value in request.POST.items():
                data_dict[key] = value

            # transform the data for 'first occurrence' and 'reported date' into datetime objects
            first_occurrence_date = datetime(
                        year=int(data_dict['first_occurrence_date_year']),
                        month=int(data_dict['first_occurrence_date_month']),
                        day=int(data_dict['first_occurrence_date_day'])
                    )
            reported_date = datetime(
                        year=int(data_dict['reported_date_year']),
                        month=int(data_dict['reported_date_month']),
                        day=int(data_dict['reported_date_day'])
                )

            # append the datetime objects into the data dictionary
            data_dict["first_occurrence_date"] = first_occurrence_date
            data_dict["reported_date"] = reported_date

            # Django Form Boolean field does not register a False value and remove the field instead.
            # Hence, if the Boolean fields is not in the dictionary, add it in.
            if 'is_crime' not in data_dict:
                data_dict["is_crime"] = False
            if 'is_traffic' not in data_dict:
                data_dict["is_traffic"] = False

            # Get the Neighbourhood object with corresponding id
            neighbourhood = Neighbourhood.objects.get(id = data_dict["neighbourhood"])

            # final data as a dictionary format to pass into our Serializer
            data = {
            "first_occurrence_date": data_dict["first_occurrence_date"],
            "reported_date": data_dict["reported_date"],
            "is_crime": data_dict["is_crime"],
            "is_traffic": data_dict["is_traffic"],
            "location": {
            "incident_address": data_dict["incident_address"],
            "district_id": data_dict['district_id'],
            "precinct_id": data_dict['precinct_id'],
            "geo": {
            "geo_x": data_dict["geo_x"],
            "geo_y": data_dict["geo_y"],
            "geo_lon": data_dict["geo_lon"],
            "geo_lat": data_dict["geo_lat"],
            },
            "neighbourhood": {
                "id": neighbourhood.id,
                "name": neighbourhood.name
            }
            },
            "victim_count": data_dict["victim_count"],
            "offense_type": data_dict["offense_type"],
            "offense_category": data_dict["offense_category"]
            }

            # Finalised data is passed into the nested CrimeSerializer
            serializer = CrimeSerializer(data = data)

            # If the serializer is valid, save the object
            if serializer.is_valid():
                serializer.save()
                return redirect('/')
            else:
                # Otherwise, print the serializers in console and redirect back to the form
                print(serializer.errors)
                return redirect('/api1')

        else:
            # if the form is not valid, render it again with the errors:
            return render(request, 'incidents/new_crime.html', {
                'crime_form': crime_form,
                'location_form': location_form,
                'geolocation_form': geolocation_form,
            })

class HotSpots(generics.ListCreateAPIView):
    """
    List the neighbourhoods that see the most specified crimes in a given year (2023).
    Accepts an offense_category_short parameter to customize the crime type.
    """
    serializer_class = NeighbourhoodSerializer

    # override the queryset method
    def get_queryset(self):
        id = self.kwargs.get('pk', 16) # default category has pk 16 (Aggravated Assault)

        # get results within the year of 2023
        start_date = date(2023,1,1)
        end_date = date(2024,1,1)

        # filter Crime by crime_type and by dates specified above
        crimes = Crime.objects.filter(offense_category = id,
                                    first_occurrence_date__range = (start_date, end_date))

        # get the locations of these crimes
        locations = crimes.values('location')

        # filter Location and return only the locations where burglary took place
        locations_hotspots = Location.objects.filter(id__in=locations)

        # get a queryset of the corresponding neighbourhoods
        neighbourhoods = locations_hotspots.values('neighbourhood')

        # aggregate the neighbourhood by count and order by descending
        neighbourhood_aggregated = neighbourhoods.annotate(count = Count('neighbourhood')).order_by('-count')[0:10]

        # filter Neighbourhood and return the top 10 neighbourhoods with the ids
        hotspots = Neighbourhood.objects.filter(id__in = neighbourhood_aggregated.values('neighbourhood'))

        return hotspots # return the hotsots as the queryset



class MotorTheftFastestResponse(generics.ListCreateAPIView):
    """
    List the locations with the fastest response when a motor vehicle is stolen.
    """
    # get the OffenseType object where short name matches 'theft-of-motor-vehicle'

    serializer_class = LocationSerializer
    def get_queryset(self):

        motor_theft = get_object_or_404(OffenseType, offense_type_short = "theft-of-motor-vehicle")


        # get the crimes that involves theft of a motor vehicle
        motor_crimes = Crime.objects.filter(offense_type = motor_theft)

        # get the time difference between the reported time and the time of occurence of the incident
        lead_time = motor_crimes.annotate(difference = (F("reported_date") -
                                        F("first_occurrence_date"))).order_by('-difference')

        # calculate the average lead time between incident and response
        avg = lead_time.aggregate(average = Avg("difference"))

        # get the Crime objects where lead time is below average (fast)
        fast_response = lead_time.filter(difference__lte = avg['average'])

        # get the corresponding Location objects
        locations = Location.objects.filter(id__in=fast_response.values('location'))[0:10]

        return locations
    # queryset = locations



class WhiteCollarWeekend(generics.ListCreateAPIView):
    """
    List the type of White Collar offenses that are committed on the weekends
    """
    serializer_class = OffenseTypeSerializer
    def get_queryset(self):

        # get the OffenseCategory object where short name matches "white-collar-crime"
        crime_type = OffenseCategory.objects.get(offense_category_short = "white-collar-crime")

        # check for all White Collar crimes
        white_collar_crime = Crime.objects.filter(offense_category = crime_type)

        # check for crimes that happened either on a Saturday (6) or a Sunday (7) using week_day method on the datetime object
        weekend_crimes = white_collar_crime.filter(Q(first_occurrence_date__week_day=6) | Q(first_occurrence_date__week_day=7))

        # get the OffenseType objects of these crimes that took place on the weekend
        white_collar_offense_types = OffenseType.objects.filter(id__in=weekend_crimes.values('offense_type'))

        return white_collar_offense_types
        # queryset = white_collar_offense_types


class NeighbourhoodsWithDrugAssault(generics.ListCreateAPIView):
    """
    List the neighbourhoods where either drugs and aggravated assault is prevelant
    """
    serializer_class = NeighbourhoodSerializer
    def get_queryset(self):

    # get the OffenseType object where short name matches "drug-poss-paraphernalia"
        crime_type_drugs = OffenseType.objects.get(offense_type_short = "drug-poss-paraphernalia")

        # get the OffenseType object where short name matches "aggravated-assault"
        crime_type_assault = OffenseType.objects.get(offense_type_short = "aggravated-assault")

        # filter the Crime objects where possession of drugs is involved and get the corresponding neighbourhood
        drug_in_location = Crime.objects.filter(offense_type = crime_type_drugs).values('location')

        # filter the Crime objects where assault is involved and get the corresponding neighbourhood
        assault_in_location = Crime.objects.filter(offense_type = crime_type_assault).values('location')

        drug_in_neighbourhoods = Location.objects.filter(id__in=drug_in_location)
        assault_in_neighbourhoods = Location.objects.filter(id__in=assault_in_location)

        # use union to get the neighbourhoods where EITHER or BOTH drugs and assaults happened
        drug_assault_neighbourhoods = drug_in_neighbourhoods.union(assault_in_neighbourhoods)

        # get the neighbourhoods where possession of drugs or aggravated assault occurred
        # queryset = Neighbourhood.objects.filter(id__in=drug_assault_neighbourhoods.values('neighbourhood'))

        return  Neighbourhood.objects.filter(id__in=drug_assault_neighbourhoods.values('neighbourhood'))



class GeolocationOfMurders(generics.ListCreateAPIView):
    """
    List the 5 cloesest geolocation to the first murder that took place
    """
    serializer_class = GeolocationSerializer
    def euclidean_dist(self, p1, p2):
        """
        Get the distance between two points
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def get_queryset(self):
        # get the OffenseCategory object where short name matches "murder"
        crime_type = OffenseCategory.objects.get(offense_category_short = "murder")

        # get all the Crime objects that matches "murder" and order by when they occurred
        murder_crimes = Crime.objects.filter(offense_category = crime_type).values('location').order_by('first_occurrence_date')

        # get the earliest murder
        first_murder =  murder_crimes[0]

        # get the Geolocation object of the earliest murder from the Location object
        first_murder_geolocation = Location.objects.get(id = first_murder['location']).geo

        # get the coordinates in a tuple for computation later
        first_murder_coords = (first_murder_geolocation.geo_lon,first_murder_geolocation.geo_lat)

        # get all the murder locations
        murder_locations = Location.objects.filter(id__in=murder_crimes)

        # get all the murder geolocations
        murder_geolocations = Geolocation.objects.filter(id__in=murder_locations)

        # get the coordinates of all the murder geolocations
        coordinates = murder_geolocations.values_list()

        # get the reference point as the first murder's geolocation
        reference_point = first_murder_coords

        # a list to hold all the distances
        distances = []

        # for each coordinate, calculate the distance from the first murder's location
        for coord in coordinates:
            # use euclidean distance defined above
            distance = self.euclidean_dist(reference_point, (coord[3], coord[4]))
            if distance == 0: # if the reference point is itself
                continue      # skip this iteration
            distances.append((distance, coord)) # add these coordinates to the list

        # sort the distances
        distances.sort(key=lambda x: x[0])

        # get the geo_id for the closest locations
        closest_geocoordinates = [coord[1][0] for coord in distances[:5]]

        closest_geolocations = Geolocation.objects.filter(id__in=closest_geocoordinates)

        return closest_geolocations


class NeighbourhoodDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer

class OffenseTypeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    List the first five offense types, or create a new offense type
    """
    queryset = OffenseType.objects.all()[:5]
    serializer_class = OffenseTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class GeolocationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer