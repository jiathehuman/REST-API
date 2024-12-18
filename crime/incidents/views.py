from rest_framework import mixins, generics, permissions
from django.contrib.auth.models import User
from django.db.models import Count, F, Value, Case, When, IntegerField, Q
from datetime import date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Avg
from django.db.models.functions import Sqrt
import math
from django.db import transaction

from .models import *
from .serializers import *
# from .permissions import ReadOnlyOrIsOwner

# Reference: https://www.django-rest-framework.org/tutorial/3-class-based-views/
# Reference for aggregation: https://docs.djangoproject.com/en/5.1/topics/db/aggregation/

@api_view(['Get','POST'])
def NewCrime(request):
    """"
    List of crimes with the option to POST (create a new crime). Validations is done through serializers
    """
    if request.method == 'GET':
        crimes = Crime.objects.filter().order_by('-first_occurrence_date')[0:5]
        serializer = CrimeSerializer(crimes, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CrimeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BurglaryHotSpots(generics.ListCreateAPIView):
    """
    List the neighbourhoods that see the most burglary in the year 2023
    """
    # get the OffenseCategory object where short name matches 'burglary'
    crime_type = OffenseCategory.objects.get(offense_category_short = "burglary")

    # get results within the year of 2023
    start_date = date(2023,1,1)
    end_date = date(2024,1,1)

    # filter Crime by crime_type and by dates specified above
    crimes = Crime.objects.filter(offense_category = crime_type,
                                  first_occurrence_date__range = (start_date, end_date))

    # get the locations of these crimes
    locations = crimes.values('location')

    # filter Location and return only the locations where burglary took place
    locations_burglary = Location.objects.filter(id__in=locations)

    # get a queryset of the corresponding neighbourhoods
    neighbourhoods = locations_burglary.values('neighbourhood')

    # aggregate the neighbourhood by count and order by descending
    neighbourhood_aggregated = neighbourhoods.annotate(count = Count('neighbourhood')).order_by('-count')[0:10]

    # filter Neighbourhood and return the top 10 neighbourhoods with the ids
    hotspots_burglary = Neighbourhood.objects.filter(id__in = neighbourhood_aggregated.values('neighbourhood'))
    # return the neighbourhoods - the final list of neighbourhoods that see the most burglary
    queryset =  hotspots_burglary
    serializer_class = NeighbourhoodSerializer


class MotorTheftFastestResponse(generics.ListCreateAPIView):
    """
    List the locations that see the fastest response when a motor vehicle is stolen
    """
    # get the OffenseType object where short name matches 'theft-of-motor-vehicle'
    motor_theft = OffenseType.objects.get(offense_type_short = "theft-of-motor-vehicle")

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

    queryset = locations
    serializer_class = LocationSerializer

class WhiteCollarWeekend(generics.ListCreateAPIView):
    """
    List the type of White Collar offenses that are committed on the weekends
    """
    # get the OffenseCategory object where short name matches "white-collar-crime"
    crime_type = OffenseCategory.objects.get(offense_category_short = "white-collar-crime")

    # check for all White Collar crimes
    white_collar_crime = Crime.objects.filter(offense_category = crime_type)

    # check for crimes that happened either on a Saturday (6) or a Sunday (7) using week_day method on the datetime object
    weekend_crimes = white_collar_crime.filter(Q(first_occurrence_date__week_day=6) | Q(first_occurrence_date__week_day=7))

    # get the OffenseType objects of these crimes that took place on the weekend
    white_collar_offense_types = OffenseType.objects.filter(id__in=weekend_crimes.values('offense_type'))

    queryset = white_collar_offense_types
    serializer_class = OffenseTypeSerializer

class NeighbourhoodsWithDrugAssault(generics.ListCreateAPIView):
    """
    List the neighbourhoods where either drugs and aggravated assault is prevelant
    """
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

    drug_assault_neighbourhoods = drug_in_neighbourhoods.union(assault_in_neighbourhoods)

    # get the neighbourhoods where possession of drugs or aggravated assault occurred
    queryset = Neighbourhood.objects.filter(id__in=drug_assault_neighbourhoods.values('neighbourhood'))
    serializer_class = NeighbourhoodSerializer

class GeolocationOfMurders(generics.ListCreateAPIView):
    """List the 5 cloesest geolocation to the first murder that took place"""
    def euclidean_dist(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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
        distance = euclidean_dist(reference_point, (coord[3], coord[4]))
        if distance == 0: # if the reference point is itself
            continue      # skip this iteration
        distances.append((distance, coord)) # add these coordinates to the list

    # sort the distances
    distances.sort(key=lambda x: x[0])

    # get the geo_id for the closest locations
    closest_geocoordinates = [coord[1][0] for coord in distances[:5]]

    closest_geolocations = Geolocation.objects.filter(id__in=closest_geocoordinates)

    queryset = closest_geolocations
    serializer_class = GeolocationSerializer



class OffenseTypeList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = OffenseType.objects.all()
    serializer_class = OffenseTypeSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class OffenseTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = OffenseType.objects.all()
    serializer_class = OffenseTypeSerializer

class OffenseCategoryList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = OffenseCategory.objects.all()
    serializer_class = OffenseCategorySerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class OffenseCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = OffenseCategory.objects.all()
    serializer_class = OffenseCategorySerializer
###
class NeighbourhoodList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer


class NeighbourhoodDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
###
###
class GeolocationList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = Geolocation.objects.all()[0:10]
    serializer_class = GeolocationSerializer


class GeolocationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer
###
###
class LocationList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = Location.objects.all()[0:5]
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
###

class CrimeList(generics.ListCreateAPIView):
    """
    Get list of crimes.
    """
    queryset = Crime.objects.all()[:10]
    serializer_class = CrimeSerializer

class CrimeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer

class ProbationViolationList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """"
    List of high collar crimes.
    """
    queryset = Crime.objects.filter(offense_type__offense_type_short__exact = 'probation-violation')
    serializer_class = CrimeSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class VirginiaVillage_List(generics.ListCreateAPIView):
    """"
    List of high collar crimes.
    """
    queryset = Location.objects.filter(neighbourhood__name__exact = 'virginia-village')
    serializer_class = LocationSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



# class CrimeDisprecancy(generics.RetrieveUpdateDestroyAPIView):
#     # crimes_with_victims = Crime.objects.filter(victim_count__gt=0)
#     # total_crimes = Crime.objects.all().count()
#     # total_victims = crimes_with_victims.aggregate(victims=models.Sum('victim_count'))['victims']
#     # discrepancy = total_victims - total_crimes

#     locations_with_multiple_crimes = Location.objects.annotate(crime__count=models.Count('crime')) \
#                                                .filter(crime__count__gt=1)
#     correlated_crimes = Crime.objects.filter(location__in=locations_with_multiple_crimes) \
#                                     .select_related('offense_type') \
#                                     .distinct('offense_type')

#     queryset = correlated_crimes






# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, ReadOnlyOrIsOwner]


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, ReadOnlyOrIsOwner]

# class OffenseTypeList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     """
#     List all offense types, or create a new offense type
#     """
#     queryset = Offense_type.objects.all()
#     serializer_class = OffenseTypeSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# class OffenseTypeDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     """
#     Retrieve, update or delete an offense type.
#     """
#     queryset = Offense_type.objects.all()
#     serializer_class = OffenseTypeSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
