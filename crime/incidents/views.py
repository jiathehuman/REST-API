from rest_framework import mixins
from rest_framework import generics

from .models import *
from .serializers import *

# Reference: https://www.django-rest-framework.org/tutorial/3-class-based-views/

class OffenseTypeList(generics.ListCreateAPIView):
    """
    List all offense types, or create a new offense type
    """
    queryset = OffenseType.objects.all()
    serializer_class = OffenseTypeSerializer


class OffenseTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an offense type.
    """
    queryset = OffenseType.objects.all()
    serializer_class = OffenseTypeSerializer

class CrimeList(generics.ListCreateAPIView):
    """
    Get list of crimes.
    """
    queryset = Crime.objects.all()[:10]
    serializer_class = CrimeSerializer

class HighCollarCrimeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """"
    List of high collar crimes.
    """
    queryset = Crime.objects.filter(offense_type__offense_type_short__exact = 'probation-violation')
    serializer_class = CrimeSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class LocationList(generics.ListCreateAPIView):
    """"
    List of high collar crimes.
    """
    queryset = Location.objects.all()[:10]
    # queryset = Location.objects.filter(neighbourhood__name__exact = 'virginia-village')
    serializer_class = LocationSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
