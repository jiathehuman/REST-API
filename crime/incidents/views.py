from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

# Create your views here.
@csrf_exempt
def offense_type_list(request):
    """
    List all offense types, or create a new offense type
    """
    if request.method == 'GET':
        offense_types = Offense_type.objects.all()
        serializer = Offense_typeSerializer(offense_types, many = True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Offense_typeSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)