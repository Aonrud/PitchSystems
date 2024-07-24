from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pitches.models import *
from decimal import Decimal


class IntervalTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.interval = Interval.objects.create(
            name="Perfect Fifth",
            description="A just-intonation perfect fifth",
            cents=Decimal(str(702)),
            ratio_numerator=3,
            ratio_denominator=2,
        )

    def test_api_interval_listview(self):
        response = self.client.get(reverse("interval_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Interval.objects.count(), 1)
        self.assertContains(response, self.interval)

    def test_api_interval_detailview(self):
        response = self.client.get(
            reverse("interval_single", kwargs={"pk": self.interval.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Interval.objects.count(), 1)
        self.assertContains(response, self.interval)
