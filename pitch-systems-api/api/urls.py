from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from .views import *


urlpatterns = [
    path(
        "frequencies/<str:frequencies>/",
        FrequenciesView.as_view(),
        name="interval_frequencies",
    ),
    path("interval/<int:pk>/", IntervalSingleView.as_view(), name="interval_single"),
    path("intervals/", IntervalListView.as_view(), name="interval_list"),
    path("intervals/<str:frequencies>/", IntervalListView.as_view(), name="intervals_frequencies"),
    path("scale/<int:pk>/", ScaleSingleView.as_view(), name="scale_single"),
    path("scales/", ScaleListView.as_view(), name="scale_list"),
    path("scales/<str:intervals>/", ScaleSingleView.as_view(), name="scale_intervals"),
]
