from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('',views.offense_type_list),
    # path('<int:pk>',views.offense_type_detail),
    path('offense-type/',views.OffenseTypeList.as_view()),
    path('offense-type/<int:pk>/', views.OffenseTypeDetail.as_view()),
    path('crime/',views.CrimeList.as_view()),
    path('crime/filtered',views.HighCollarCrimeList.as_view()),
    path('location',views.LocationList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)