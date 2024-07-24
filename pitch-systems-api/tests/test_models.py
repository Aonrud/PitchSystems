from django.test import TestCase
from django.urls import reverse
from pitches.models import *

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

test_scales = [
    Scale.objects.create(
        name="12-ET Major",
        description="The major scale in 12-tone equal temperament",
    )
]


class IntervalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.interval = test_intervals[0]

    def test_interval_fields_valid(self):
        self.assertEqual(self.interval.name, "Rational Interval")
        self.assertEqual(self.interval.description, "A just-intonation perfect fifth")
        self.assertEqual(self.interval.cents, 702)
        self.assertEqual(self.interval.ratio_numerator, 3)
        self.assertEqual(self.interval.ratio_denominator, 2)


class ScaleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.scale = test_scales[0]
        cls.intervals = test_intervals  
        cls.scale.intervals.add(cls.intervals[0])
        cls.scale.intervals.add(cls.intervals[1])

    def test_scale_fields_valid(self):
        self.assertEqual(self.scale.name, "12-ET Major")
        self.assertEqual(
            self.scale.description, "The major scale in 12-tone equal temperament"
        )
        self.assertListEqual([str(interval) for interval in self.scale.intervals.all()], ["Rational Interval", "Cents interval"])
        # self.assertEqual(list(self.scale.intervals.all()), self.intervals)
