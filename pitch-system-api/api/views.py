from rest_framework import viewsets
from pitches.models import *
from .serializers import *


class IntervalView(viewsets.ModelViewSet): 
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer