from django.test import TestCase
from django.urls import reverse
from .models import *


class IntervalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.interval = Interval.objects.create(
            name="Perfect Fifth",
            description="A just-intonation perfect fifth",
            cents=702,
            ratio_numerator=3,
            ratio_denominator=2
        )

    def test_interval_fields_valid(self):
        self.assertEqual(self.interval.name, "Perfect Fifth")
        self.assertEqual(self.interval.description, "A just-intonation perfect fifth")
        self.assertEqual(self.interval.cents, 702)
        self.assertEqual(self.interval.ratio_numerator, 3)
        self.assertEqual(self.interval.ratio_denominator, 2)
