from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from .views import *
from drf_spectacular.views import ( SpectacularAPIView, SpectacularSwaggerView )


urlpatterns = [ 
    path("interval/<int:pk>/", IntervalSingle.as_view(), name="interval_single"),
    path("intervals/", IntervalList.as_view(), name="interval_list"),
    path("frequencies/<frequencies>/", FrequenciesView.as_view(), name="interval_frequencies")
]