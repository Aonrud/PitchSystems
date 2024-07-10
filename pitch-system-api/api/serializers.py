from rest_framework import serializers
from pitches.models import *

class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        fields = ("name", "description", "cents", "ratio_enumerator", "ratio_denominator")