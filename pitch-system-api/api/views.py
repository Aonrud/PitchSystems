from rest_framework import generics
from pitches.models import *
from .serializers import *


class IntervalAPIView(generics.ListAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer