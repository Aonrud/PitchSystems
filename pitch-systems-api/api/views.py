from rest_framework import generics, viewsets, views, exceptions
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

    serializer_class = FrequencySerializer

    def get(self, request, **kwargs):
        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]
        frequencies = self.kwargs["frequencies"].split(
            settings.PS_SETTINGS["LIST_STRING_SEPARATOR"]
        )

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

        # TODO: Add logic for ratio. Custom QuerySet or model method? See if it can be done in standard filter method

        # Filter by cents
        cents_filter = self.request.query_params.get("cents")
        if cents_filter:
            cents = cents_filter.split(settings.PS_SETTINGS["LIST_STRING_SEPARATOR"])

            try:
                cents_valid = list(map(float, cents))
            except:
                raise exceptions.ValidationError({"error": "Invalid cents value"})

            filters = {}
            filters[f"cents__in"] = cents_valid
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

            try:
                intervals_valid = list(map(int, intervals))
            except:
                raise exceptions.ValidationError(
                    {"error": "Invalid id value. Not an integer."}
                )

            intersections = [
                Scale.objects.filter(intervals=interval)
                for interval in intervals_valid[1:]
            ]
            queryset = Scale.objects.filter(intervals=intervals_valid[0]).intersection(
                *intersections
            )
        return queryset
