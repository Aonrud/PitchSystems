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

test_systems = [
    System.objects.create(
        name="12-Tone Equal Temperament",
        description="Divides the octave into 12 equal semitones of 100 cents.",
    )
]


class IntervalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.system = test_systems[0]
        cls.system.save()
        cls.interval = test_intervals[0]
        cls.interval.save()
        cls.interval_name = IntervalName.objects.create(
            name="Alternative Name",
            description=None,
            interval=cls.interval,
            system=cls.system,
        )

    def test_interval_fields_valid(self):
        self.assertEqual(self.interval.name, "Rational Interval")
        self.assertEqual(self.interval.description, "A just-intonation perfect fifth")
        self.assertEqual(self.interval.cents, 702)
        self.assertEqual(self.interval.ratio_numerator, 3)
        self.assertEqual(self.interval.ratio_denominator, 2)

    def test_interval_name_fields_valid(self):
        self.assertEqual(self.interval_name.name, "Alternative Name")
        self.assertIsNone(self.interval_name.description)


class ScaleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.intervals = test_intervals
        for interval in cls.intervals:
            interval.save()

        cls.system = test_systems[0]
        cls.system.save()
        cls.scale = Scale.objects.create(
            name="12-ET Major",
            description="The major scale in 12-tone equal temperament",
            system=cls.system,
        )
        cls.scale.intervals.set(cls.intervals)

    def test_scale_fields_valid(self):
        self.assertEqual(self.scale.name, "12-ET Major")
        self.assertEqual(
            self.scale.description, "The major scale in 12-tone equal temperament"
        )
        self.assertEqual(self.scale.system, self.system)
        self.assertListEqual(list(self.scale.intervals.all()), self.intervals)


class NomenclatureTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nomenclature = Nomenclature.objects.create(
            name="Term", description="Definition"
        )

    def test_nomenclature_fields_valid(self):
        self.assertEqual(self.nomenclature.name, "Term")
        self.assertEqual(self.nomenclature.description, "Definition")
