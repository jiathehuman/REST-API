from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name = 'index'), # index page
    path('api1',views.NewCrime, name = 'api1'),
    path('api2/<int:pk>/',views.HotSpots.as_view(), name = 'api2'),
    path('api3',views.MotorTheftFastestResponse.as_view(), name = 'api3'),
    path('api4', views.WhiteCollarWeekend.as_view(), name = 'api4'),
    path('api5',views.NeighbourhoodsWithDrugAssault.as_view(), name = 'api5'),
    path('api6',views.GeolocationOfMurders.as_view(), name = 'api6'),
    path('neighbourhood/<int:pk>/',views.NeighbourhoodDetail.as_view(), name = 'neighbourhood'),
    path('offense-type/',views.OffenseTypeList.as_view(), name = 'offense_type'),
    path('geolocation/<int:pk>/', views.GeolocationDetail.as_view(), name = 'geolocation')
]