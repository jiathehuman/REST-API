from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Offense_type)
admin.site.register(Offense_category)
admin.site.register(Neighbourhood)
admin.site.register(Geolocation)
admin.site.register(Location)
admin.site.register(Crime)