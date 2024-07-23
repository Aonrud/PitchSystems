from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from pitches.models import *
from .serializers import *
from utils import conversions
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class IntervalListView(generics.ListAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer


class IntervalSingleView(generics.RetrieveAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer


class ScaleSingleView(generics.RetrieveAPIView):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer


class ScaleListView(generics.ListAPIView):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer


class FrequenciesView(APIView):
    http_method_names = ["get"]

    def validate_freqs(freqs: str) -> bool:
        """
        Validate a comma-separated list of frequencies
        """
        return True

    def get(self, request, *args, **kwargs) -> Response:
        """
        Return all information about a given set of frequencies
        """
        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]
        frequencies = self.kwargs["frequencies"].split("+")

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
            inputs.append(conversions.cents_between(float(root), float(freq)))

        for input in inputs:
            intervals = Interval.objects.filter(cents__gte=input - tolerance).filter(
                cents__lte=input + tolerance
            )
            serializer = IntervalSerializer(intervals, many=True)

            closest = min(
                intervals,
                key=lambda interval: abs(float(interval.cents) - float(input)),
            )
            scale_interval_matches.append(closest.id)

            output["response"]["intervals"]["{:.4f}".format(input)] = {
                "closest": closest.id,
                "matches": serializer.data,
            }

        # Get matching scales
        scales = Scale.objects.filter(intervals__in=scale_interval_matches)
        serializer = ScaleSerializer(scales, many=True)
        output["response"]["scales"] = serializer.data

        return Response(output)
