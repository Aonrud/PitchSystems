from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from pitches.models import *
from .serializers import *
from utils import conversions
from django.conf import settings


class IntervalList(generics.ListAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer
    # lookup_field = 'cents'


class IntervalSingle(generics.RetrieveAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer
    # lookup_field = 'cents'


class FrequenciesView(APIView):
    http_method_names = ["get"]

    def validate_freqs(freqs: str) -> bool:
        """
        Validate a comma-separated list of frequencies
        """
        return

    def get(self, request, *args, **kwargs) -> Response:
        """
        Return all information about a given set of frequencies
        """
        tolerance = settings.PS_SETTINGS["CENTS_TOLERANCE"]
        frequencies = self.kwargs["frequencies"].split(",")
        scale = sorted(set(frequencies))  # Ordered list of unique frequencies
        inputs = []
        output = {
            "request": { 
                "frequencies": frequencies,
                "scale": scale
             },
             "response": {
                "intervals": {},
                "scales": {}
             }
        }

        root = scale[0]

        # Get interval from first
        for freq in scale[1:]:
            inputs.append(conversions.cents_between(float(root), float(freq)))

        for input in inputs:
            intervals = Interval.objects.filter(cents__gte=input - tolerance).filter(
                cents__lte=input + tolerance
            )
            serializer = IntervalSerializer(intervals, many=True)

            output["response"]["intervals"]["{:.4f}".format(input)] = serializer.data

        return Response(output)
