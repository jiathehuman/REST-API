from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name = 'index'),
    path('api1',views.NewCrime),
    path('api2/<int:pk>/',views.HotSpots.as_view(), name = 'api2'),
    path('api3',views.MotorTheftFastestResponse.as_view()),
    path('api4', views.WhiteCollarWeekend.as_view()),
    path('api5',views.NeighbourhoodsWithDrugAssault.as_view()),
    path('api6',views.GeolocationOfMurders.as_view()),
    path('neighbourhood/<int:pk>/',views.NeighbourhoodDetail.as_view()),
    path('offense-type/',views.OffenseTypeList.as_view()),

    # path('location/',views.LocationList.as_view()),
    # path('geolocation/', views.GeolocationList.as_view()),
    # path('crime/',views.CrimeList.as_view()),
    # path('crime/<int:pk>',views.CrimeDetail.as_view()),
    # path('location/<int:pk>',views.LocationDetail.as_view()),
    path('geolocation/<int:pk>/', views.GeolocationDetail.as_view()),

    # path('offense-type/<int:pk>/', views.OffenseTypeDetail.as_view()),
    # path('offense-category/',views.OffenseCategoryList.as_view()),
    # path('offense-category/<int:pk>/', views.OffenseCategoryDetail.as_view()),
    # path('neighbourhood/',views.NeighbourhoodList.as_view()),

    # path('crime/<int:pk>',views.CrimeDetail.as_view()),
    # path('location/virginia_village',views.VirginiaVillage_List.as_view()),
    # path('crime/probation-list',views.ProbationViolationList.as_view()),
    # path('api2',views.crime_disprecancy),
]