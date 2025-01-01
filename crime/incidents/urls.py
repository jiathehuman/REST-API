from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name = 'index'), # index page
    path('api1',views.NewCrime, name = 'api1'), # POST a new crime
    path('api2/<int:pk>/',views.HotSpots.as_view(), name = 'api2'), # get all the Hot Spots where a certain type of crime happened
    path('api3',views.MotorTheftFastestResponse.as_view(), name = 'api3'), # get the neighbourhoods that sees the fastest response to motor theft
    path('api4', views.WhiteCollarWeekend.as_view(), name = 'api4'), # get the white collar crimes committed on weekends
    path('api5',views.NeighbourhoodsWithDrugAssault.as_view(), name = 'api5'), # get the neighbourhoods where either drug or assault is prevelant
    path('api6',views.GeolocationOfMurders.as_view(), name = 'api6'), # get the nearest locations to the first murder
    path('neighbourhood/<int:pk>/',views.NeighbourhoodDetail.as_view(), name = 'neighbourhood'), # get the neighbourhood detail view
    path('offense-type/',views.OffenseTypeList.as_view(), name = 'offense_type'), # get the offese type as a list view
    path('geolocation/<int:pk>/', views.GeolocationDetail.as_view(), name = 'geolocation'), # get the geolocation detail view
    path('crime/',views.CrimeList.as_view()), # crime list as view
]