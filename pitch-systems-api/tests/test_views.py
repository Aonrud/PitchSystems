from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pitches.models import *
from django.utils.http import urlencode
from django.core import exceptions


def reverse_querystring(
    view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None
):
    """Custom reverse to handle query strings.
    See: https://gist.github.com/benbacardi/227f924ec1d9bedd242b

    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    """
    base_url = reverse(
        view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
    )
    if query_kwargs:
        return "{}?{}".format(base_url, urlencode(query_kwargs))
    return base_url


test_intervals = [
    Interval.objects.create(
        name="Rational Interval",
        description="A just-intonation perfect fifth",
        cents=702,
        ratio_numerator=3,
        ratio_denominator=2,
    ),
    Interval.objects.create(
        name="Cents interval",
        description="A 12-ET perfect fifth",
        cents=700,
    ),
]

test_system = System.objects.create(
    name="12-Tone Equal Temperament",
    description="Divides the octave into 12 equal semitones of 100 cents.",
)


class FrequencyTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.freqs_valid = "327.0320,261.6256,392.4384"  # Major triad, unsorted
        cls.freqs_invalid = "327.0320,261.6256,392.4384,abc"

    def test_frequency_view_valid(self):
        response = self.client.get(
            reverse("frequency_cents", kwargs={"frequencies": self.freqs_valid})
        )
        expected = {
            "261.6256-327.0320": "386.3137",
            "261.6256-392.4384": "701.9550",
        }
        self.assertEqual(response.data, expected)

    def test_frequency_view_invalid(self):
        response = self.client.get(
            reverse("frequency_cents", kwargs={"frequencies": self.freqs_invalid})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IntervalTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.intervals = test_intervals
        for interval in cls.intervals:
            interval.save()
        cls.system = test_system
        cls.system.save()
        cls.names = [
            IntervalName.objects.create(
                name="Name with a system",
                description=None,
                interval=cls.intervals[0],
                system=cls.system,
            ),
            IntervalName.objects.create(
                name="Name without system",
                description="This one has a description",
                interval=cls.intervals[0],
            ),
        ]

    def test_api_interval_listview(self):
        response = self.client.get(reverse("interval_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.intervals[0])
        self.assertContains(response, self.intervals[1])

    def test_api_interval_detailview(self):
        response = self.client.get(
            reverse("interval_single", kwargs={"pk": self.intervals[0].id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.intervals[0])

    def test_api_interval_filter_cents_valid(self):
        response = self.client.get(
            reverse_querystring("interval_list", query_kwargs={"cents": "700,400"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, self.intervals[1])
        self.assertNotContains(response, self.intervals[0])

    def test_api_interval_filter_cents_invalid(self):
        response = self.client.get(
            reverse_querystring("interval_list", query_kwargs={"cents": "abc,400"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ScaleTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.intervals = test_intervals
        for interval in cls.intervals:
            interval.save()
        cls.system = test_system
        cls.system.save()
        cls.scales = [
            Scale.objects.create(
                name="12-ET Major",
                description="The major scale in 12-tone equal temperament",
                system=cls.system,
            ),
            Scale.objects.create(
                name="Test scale",
                description=None,
                system=cls.system,
            ),
        ]
        cls.scales[0].intervals.set([cls.intervals[0]])
        cls.scales[1].intervals.set(cls.intervals)

    def test_api_scales_listview(self):
        response = self.client.get(reverse("scale_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.scales[0])
        self.assertContains(response, self.scales[1])

    def test_api_scales_detailview(self):
        response = self.client.get(
            reverse("scale_single", kwargs={"pk": self.scales[0].id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.scales[0])

    def test_api_scales_filter_intervals_valid(self):
        interval_ids = [i.id for i in self.intervals]

        # A valid request for both test intervals should return only the second scale
        response = self.client.get(
            reverse(
                "scale_intervals",
                kwargs={"intervals": ",".join(list(map(str, interval_ids)))},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_api_scales_filter_intervals_invalid(self):
        interval_ids = [i.id for i in self.intervals]
        interval_ids.append("badvalue")

        response = self.client.get(
            reverse(
                "scale_intervals",
                kwargs={"intervals": ",".join(list(map(str, interval_ids)))},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
