from rest_framework import serializers
from pitches.models import *
from drf_spectacular.utils import extend_schema, OpenApiParameter   

class IntervalNameSerializer(serializers.ModelSerializer):
    # system = serializers.StringRelatedField()

    class Meta:
        model = IntervalName
        fields = ("id", "name", "description", "system")


class IntervalSerializer(serializers.ModelSerializer):
    """
    Serializes an interval with full information.
    """

    ratio: str = serializers.SerializerMethodField()
    additional_names = IntervalNameSerializer(many=True, read_only=True)

    # TODO: If set, the name associated with this system will be displayed instead of the default
    # system_id = None

    # def set_system(self, int: id) -> None:
    #     self.system_id = id

    # if system_id:
    #     name = [o for o in additional_names.data if o.system == system_id][0]

    def get_ratio(self, obj) -> str:
        if obj.ratio_numerator is None:
            return None
        else:
            return f"{obj.ratio_numerator}:{obj.ratio_denominator}"

    class Meta:
        model = Interval
        fields = ("id", "name", "description", "cents", "ratio", "additional_names")


class ScaleSerializer(serializers.ModelSerializer):
    intervals = IntervalSerializer(many=True, read_only=True)
    # system = serializers.StringRelatedField()

    class Meta:
        model = Scale
        fields = ("id", "name", "description", "system", "intervals")


class FrequencySerializer(serializers.Serializer):
    """
    Serializer to validate frequency list URL parameter
    """

    value = serializers.FloatField(required=True)

class BasicSerializer(serializers.Serializer):
    """
    Serializer for models that only have the base model fields.
    """
    class Meta:
        model = AbstractBaseModel
        fields = ("id", "name", "description")
