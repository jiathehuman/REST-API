from rest_framework import mixins, generics, permissions
from django.contrib.auth.models import User
from django.db.models import Count, F, Value, Case, When, IntegerField, Q
from datetime import date

from .models import *
from .serializers import *
# from .permissions import ReadOnlyOrIsOwner

# Reference: https://www.django-rest-framework.org/tutorial/3-class-based-views/

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
    queryset = Geolocation.objects.all()
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
    queryset = Location.objects.all()
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



# reference for aggregation: https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
class HotSpots(generics.ListCreateAPIView):
    """
    List the hot spots for burglary in the year 2023
    """
    # get the OffenseType object where short name matches 'criminal-trespassing'
    crime_type = OffenseCategory.objects.get(offense_category_short = "burglary")

    # get results within the year of 2023
    start_date = date(2023,1,1)
    end_date = date(2024,1,1)

    # filter Crime by crime_type and by dates specified aboe
    crimes = Crime.objects.filter(offense_category = crime_type, first_occurrence_date__range = (start_date, end_date))

    locations = crimes.values('location')

    loc = Location.objects.filter(id__in=locations)

    neighbourhood = loc.values('neighbourhood')

    neighbourhood_hot = neighbourhood.values('neighbourhood').annotate(count = Count('neighbourhood')).order_by('-count')
    ids = [item['neighbourhood'] for item in neighbourhood_hot]

    hot_neighbourhoods = Neighbourhood.objects.filter(id__in=ids)
    queryset = hot_neighbourhoods
    serializer_class = NeighbourhoodSerializer


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
