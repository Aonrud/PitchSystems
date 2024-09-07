from django.db.models import F, Func
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
    Take a list of frequencies and return a list of intervals in cents between each one and a root note.

    By default, the last frequency in the list is treated as the root note ('tonic', 'do', 'finalis' etc.).
    If the root parameter is provided, intervals will be measured from that frequency.

    Note: The root note does not have to be one of the provided frequencies.
    """

    serializer_class = FrequencySerializer

    def get(self, request, **kwargs):
        frequencies = self.kwargs["frequencies"].split(
            settings.PS_SETTINGS["LIST_STRING_SEPARATOR"]
        )

        root = self.request.query_params.get("root")
        if root:
            ref_freq = root
        else:
            ref_freq = frequencies[-1]

        # Validate frequencies and raise exception
        test = FrequencySerializer(data=[{"value": x} for x in frequencies], many=True)
        test.is_valid(raise_exception=True)

        scale = sorted(set(frequencies))  # Ordered list of unique frequencies
        cents = []
        for freq in scale:
            cents.append(
                {
                    "cents": utils.format_number(
                        utils.cents_between(float(ref_freq), float(freq))
                    ),
                    "f1": utils.format_number(ref_freq),
                    "f2": utils.format_number(freq),
                }
            )
        # Get a unique list. Close frequency values can become duplicates after rounding with format_number().
        cents = list({f"{val['f1']}-{val['f2']}":val for val in cents}.values())

        return Response(cents)


class IntervalViewset(viewsets.ReadOnlyModelViewSet):
    """
    Get a list of intervals, optionally filtered to match a list of cents values.
    """

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

    def get_near(self, request, *args, **kwargs):
        """
        Get a list of intervals near the given cents value.
        An optional 'tolerance' URL parameter allows filtering how many cents difference is considered 'near'. Otherwise, the default is used.
        """

        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]

        cents = self.kwargs["cents"]
        req_tolerance = self.request.query_params.get("tolerance")

        # Set tolerance if valid, otherwise fallback to default
        if req_tolerance and req_tolerance.isnumeric():
            tolerance = int(req_tolerance)

        try:
            cents = float(cents)
        except ValueError:
            raise exceptions.ValidationError({"error": "Invalid cents value"})

        queryset = Interval.objects.all()
        filters = {}
        filters[f"cents__gte"] = cents - tolerance
        filters[f"cents__lte"] = cents + tolerance
        queryset = Interval.objects.filter(**filters)

        result = self.serializer_class(queryset, many=True)
        return Response(result.data)


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

class SystemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get a pitch system by id, or the full list.
    """

    serializer_class = SystemSerializer
    queryset = System.objects.all()

class NomenclatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get nomenclature entries or an individual term.
    """

    serializer_class = NomenclatureSerializer
    
    def get_queryset(self):
        queryset = Nomenclature.objects.all()

        # Filter by term
        term = self.kwargs.get("term")
        if term:
            queryset = Interval.objects.filter(name.lower()==term.lower())

        return queryset
