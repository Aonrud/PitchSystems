from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from pitches.models import *
from .serializers import *
from utils import conversions


class IntervalList(generics.ListAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer
    # lookup_field = 'cents'


class IntervalSingle(generics.RetrieveAPIView):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer
    # lookup_field = 'cents'


class IntervalFrequencies(APIView):
    http_method_names = ["get"]

    def validate_freqs(freqs: str) -> bool:
        """
        Validate a comma-separated list of frequencies
        """
        return

    def get(self, request, *args, **kwargs) -> Response:
        """
        Return intervals matching frequencies given in kwargs
        """
        tolerance = 5
        frequencies = sorted(
            set(self.kwargs["frequencies"].split(","))
        )  # Order list of unique frequencies
        inputs = []
        output = {}

        root = frequencies[0]

        # Get interval from first
        for freq in frequencies[1:]:
            inputs.append(conversions.cents_between(float(root), float(freq)))

        for input in inputs:
            intervals = Interval.objects.filter(cents__gte=input - tolerance).filter(
                cents__lte=input + tolerance
            )
            serializer = IntervalSerializer(intervals, many=True)

            output["{:.4f}".format(input)] = serializer.data

        return Response(output)
