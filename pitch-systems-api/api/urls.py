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
    path("frequencies/<str:frequencies>/", FrequencyView.as_view(), name="frequency_cents"),
    path("scale/<int:pk>/", ScaleViewset.as_view({'get': 'retrieve'}), name="scale_single"),
    path("scales/", ScaleViewset.as_view({'get': 'list'}), name="scale_list"),
    path("scales/<str:intervals>/", ScaleViewset.as_view({'get': 'list'}), name="scale_intervals"),
]
