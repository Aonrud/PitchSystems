from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from pitches.models import *
from .serializers import *
import utils
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class FrequencyView(views.APIView):
    """
    View to take a list of frequencies and return the list of intervals between the lowest frequency
    and each of the others.
    """

    def get(self, request, **kwargs):
        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]
        frequencies = self.kwargs["frequencies"].split(settings.PS_SETTINGS["LIST_STRING_SEPARATOR"])

        # Validate frequencies and raise exception
        test = FrequencySerializer(data=[{"value": x} for x in frequencies], many=True)
        test.is_valid(raise_exception=True)

        scale = sorted(set(frequencies))  # Ordered list of unique frequencies
        root = scale[0]
        cents = {}
        for freq in scale[1:]:
            cents[f"{root}-{freq}"] = utils.format_cents(
                utils.cents_between(float(root), float(freq))
            )
        return Response(cents)


class IntervalViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = IntervalSerializer

    def get_queryset(self):
        queryset = Interval.objects.all()

        filters = {}
        for param in ["cents", "id"]:
            value = self.request.query_params.get(param)
            if value is not None:
                filters[f"{param}__in"] = value.split(settings.PS_SETTINGS["LIST_STRING_SEPARATOR"])

        # TODO: Add logic for ratio. Custom QuerySet or model method? See if it can be done in standard filter method

        if filters:
            queryset = Interval.objects.filter(**filters)
        return queryset


class ScaleViewset(viewsets.ReadOnlyModelViewSet):
    """
    Get Scales by ID, filtered by intervals included, or the full list.
    """
    serializer_class = ScaleSerializer

    def get_queryset(self):
        queryset = Scale.objects.all()
        intervals = self.kwargs.get("intervals")
        if intervals is not None:
            intervals = intervals.split(settings.PS_SETTINGS["LIST_STRING_SEPARATOR"])
            intersections = [Scale.objects.filter(intervals = interval) for interval in intervals[1:]] 
            queryset = Scale.objects.filter(intervals = intervals[0]).intersection(*intersections)
        return queryset 


class FrequenciesView(views.APIView):
    http_method_names = ["get"]

    def validate_freqs(self, freqs: str) -> bool:
        """
        Validate a comma-separated list of frequencies
        """
        return True

    def get(self, request, *args, **kwargs) -> Response:
        """
        Return all information about a given set of frequencies
        """
        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]
        frequencies = self.kwargs["frequencies"].split(settings.PS_SETTINGS["LIST_STRING_SEPARATOR"])

        # Validate frequencies and raise exception
        test = FrequencySerializer(data=[{"value": x} for x in frequencies], many=True)
        test.is_valid(raise_exception=True)

        scale = sorted(set(frequencies))  # Ordered list of unique frequencies
        inputs = []
        output = {
            "request": {"frequencies": frequencies, "scale": scale},
            "response": {"intervals": {}, "scales": {}},
        }

        # Lowest frequency, against which to compare
        root = scale[0]

        # List of closest interval match IDs
        scale_interval_matches = []

        # Get interval from first
        for freq in scale[1:]:
            inputs.append(utils.cents_between(float(root), float(freq)))

        for input in inputs:
            intervals = Interval.objects.filter(cents__gte=input - tolerance).filter(
                cents__lte=input + tolerance
            )
            int_serializer = IntervalSerializer(intervals, many=True)

            closest = min(
                intervals,
                key=lambda interval: abs(float(interval.cents) - float(input)),
            )
            scale_interval_matches.append(closest.id)

            output["response"]["intervals"][utils.format_cents(input)] = {
                "closest": closest.id,
                "matches": int_serializer.data,
            }

        # Get matching scal es
        scales = Scale.objects.filter(intervals__in=scale_interval_matches)
        scale_serializer = ScaleSerializer(scales, many=True)
        output["response"]["scales"] = scale_serializer.data

        return Response(output)
