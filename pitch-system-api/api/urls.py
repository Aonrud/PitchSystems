from django.urls import path
from .views import IntervalAPIView

urlpatterns = [
    path("", IntervalAPIView.as_view(), name="interval_list"),
]