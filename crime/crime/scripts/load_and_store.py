import os
import sys
import django
import csv
from collections import defaultdict

sys.path.append("/Users/main/Desktop/Advanced_Web_Development/Midterms/midterm_app/crime/crime")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','crime.settings')
django.setup()

from incidents.models import *

offense_code_file = 'cleaned_offense_codes.csv'
crime_file = 'cleaned_crime.csv'
offense_type = set()
offense_category = set()
neighbourhoods = set()
geolocation = defaultdict()
location = defaultdict()
crime = defaultdict()

with open(offense_code_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.__next__()
    for row in csv_reader:
        offense_type.add((row[3],row[4]))
        offense_category.add((row[5],row[6]))

with open(crime_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.__next__()
    for row in csv_reader:
        neighbourhoods.add(row[12])
        geolocation[row[0]] = dict()
        geolocation[row[0]]['geo_x'] = row[6]
        geolocation[row[0]]['geo_y'] = row[7]
        geolocation[row[0]]['geo_lon'] = row[8]
        geolocation[row[0]]['geo_lat'] = row[9]

        location[row[0]] = dict()
        location[row[0]]['incident_address'] = row[5]
        location[row[0]]['district_id'] = row[10]
        location[row[0]]['precinct_id'] = row[11]
        location[row[0]]['neighbourhood_id'] = row[12]

        crime[row[0]] = dict()
        crime[row[0]]['first_occurrence_date'] = row[3]
        crime[row[0]]['reported_date'] = row[4]
        crime[row[0]]['is_crime'] = row[13]
        crime[row[0]]['is_traffic'] = row[14]
        crime[row[0]]['victim_count'] = row[15]
        crime[row[0]]['offense_type_id'] = row[1]
        crime[row[0]]['offense_category_id'] = row[2]

offense_type_rows = {}
offense_category_rows = {}
neighbourhoods_rows = {}
geolocation_rows = {}
location_rows = {}
crime_rows = {}

Crime.objects.all().delete()
Location.objects.all().delete()
Geolocation.objects.all().delete()
OffenseType.objects.all().delete()
OffenseCategory.objects.all().delete()
Neighbourhood.objects.all().delete()

for item in offense_type:
    row = OffenseType.objects.create(offense_type_short = item[0],
                                    offense_type_name = item[1])
    row.save()
    offense_type_rows[item[0]] = row

for item in offense_category:
    row = OffenseCategory.objects.create(offense_category_short = item[0],
                                    offense_category_name = item[1])
    row.save()
    offense_category_rows[item[0]] = row

for neighbourhood in neighbourhoods:
    row = Neighbourhood.objects.create(name = neighbourhood)
    row.save()
    neighbourhoods_rows[neighbourhood] = row


for geolocation, dict_values in geolocation.items():
    row = Geolocation.objects.create(
        geo_x = dict_values['geo_x'],
        geo_y = dict_values['geo_y'],
        geo_lon = dict_values['geo_lon'],
        geo_lat = dict_values['geo_lat']
    )
    row.save()
    geolocation_rows[geolocation] = row

for location, dict_values in location.items():
    row = Location.objects.create(
        incident_address = dict_values['incident_address'],
        district_id = dict_values['district_id'],
        precinct_id = dict_values['precinct_id'],
        geo = geolocation_rows[location],
        neighbourhood = neighbourhoods_rows[dict_values['neighbourhood_id']]
    )
    row.save()
    location_rows[location] = row

for crime, dict_values in crime.items():
    row = Crime.objects.create(
        first_occurrence_date = dict_values['first_occurrence_date'],
        reported_date = dict_values['reported_date'],
        is_crime = dict_values['is_crime'],
        is_traffic = dict_values['is_traffic'],
        victim_count = dict_values['victim_count'],
        location = location_rows[crime],
        offense_type = offense_type_rows[dict_values['offense_type_id']],
        offense_category = offense_category_rows[dict_values['offense_category_id']]
    )