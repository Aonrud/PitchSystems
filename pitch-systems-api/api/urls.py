from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from .views import *


urlpatterns = [ 
    path(
        "frequencies/<str:frequencies>/",
        FrequencyView.as_view(),
        name="interval_frequencies",
    ),
    path("interval/<int:pk>/", IntervalViewset.as_view({'get': 'retrieve'}), name="interval_single"),
    path("intervals/", IntervalViewset.as_view({'get': 'list'}), name="interval_list"),
    path("intervals/near/<str:cents>/", IntervalViewset.as_view({'get': 'get_near'}), name="intervals_near"),
    path("frequencies/<str:frequencies>/", FrequencyView.as_view(), name="frequency_cents"),
    path("scale/<int:pk>/", ScaleViewset.as_view({'get': 'retrieve'}), name="scale_single"),
    path("scales/", ScaleViewset.as_view({'get': 'list'}), name="scale_list"),
    path("scales/<str:intervals>/", ScaleViewset.as_view({'get': 'list'}), name="scale_intervals"),
    path("systems/", SystemViewSet.as_view({'get': 'list'}), name="system_list"),
    path("system/<int:pk>/", IntervalViewset.as_view({'get': 'retrieve'}), name="system_single"),
    path("nomenclature/", NomenclatureViewSet.as_view({'get': 'list'}), name="nomenclature_list"),
    path("nomenclature/<str:term>/", NomenclatureViewSet.as_view({'get': 'retrieve'}), name="nomenclature_single"),
]
