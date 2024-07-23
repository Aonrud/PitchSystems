from rest_framework import serializers
from pitches.models import *


class IntervalSerializer(serializers.ModelSerializer):
    ratio = serializers.SerializerMethodField()

    def get_ratio(self, obj):
        if obj.ratio_numerator is None:
            return None
        else:
            return f"{obj.ratio_numerator}:{obj.ratio_denominator}"

    class Meta:
        model = Interval
        fields = ("id", "name", "description", "cents", "ratio")


class ScaleSerializer(serializers.ModelSerializer):
    intervals = IntervalSerializer(many=True, read_only=True)

    class Meta:
        model = Scale
        fields = ("id", "name", "description", "intervals")


class FrequencySerializer(serializers.Serializer):
    """
    Serializer to validate frequency list URL parameter
    """

    value = serializers.FloatField(required=True)
