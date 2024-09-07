from rest_framework import serializers
from pitches.models import *
from drf_spectacular.utils import extend_schema, OpenApiParameter   

class IntervalNameSerializer(serializers.ModelSerializer):
    system = serializers.StringRelatedField()

    class Meta:
        model = IntervalName
        fields = ("id", "name", "description", "system")

class SystemSerializer(serializers.ModelSerializer):
    """
    A Pitch System.
    """
    class Meta:
        model = System
        fields = ("id", "name", "description")

class NomenclatureSerializer(serializers.ModelSerializer):
    """
    A term in the nomenclature.
    """
    class Meta:
        model = Nomenclature
        fields = ("id", "name", "description")

class IntervalSerializer(serializers.ModelSerializer):
    """
    An interval.
    """

    ratio: str = serializers.SerializerMethodField()
    additional_names = IntervalNameSerializer(many=True, read_only=True)

    # TODO: If set, the name associated with this system will be displayed instead of the default
    # system_id = None

    # def set_system(self, int: id) -> None:
    #     self.system_id = id

    # if system_id:
    #     name = [o for o in additional_names.data if o.system == system_id][0]

    def get_ratio(self, obj) -> str|None:
        if obj.ratio_numerator is None:
            return None
        else:
            return f"{obj.ratio_numerator}:{obj.ratio_denominator}"

    class Meta:
        model = Interval
        fields = ("id", "name", "description", "cents", "ratio", "additional_names")

class ScaleSerializer(serializers.ModelSerializer):
    intervals = IntervalSerializer(many=True, read_only=True)
    system = SystemSerializer()

    class Meta:
        model = Scale
        fields = ("id", "name", "description", "system", "intervals")


class FrequencySerializer(serializers.Serializer):
    """
    A valid frequency number.
    """

    value = serializers.FloatField(required=True)
