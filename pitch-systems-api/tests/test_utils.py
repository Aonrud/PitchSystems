from django.test import TestCase
import utils


class UtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cents = 400
        cls.freqs = [
            float(261.6256),  # 12-ET C4
            float(329.6276),  # 12-ET E4
        ]

    def test_cents_between(self):
        cents = utils.cents_between(self.freqs[0], self.freqs[1])
        self.assertAlmostEqual(cents, 400, 4) #Allows for float variance

    def test_cents_above(self):
        freq = utils.cents_above(self.freqs[0], 400)
        self.assertAlmostEqual(freq, self.freqs[1], 4)

    def test_format_cents(self):
        cents = utils.cents_between(4, 5)
        formatted = utils.format_cents(cents)
        self.assertEqual(formatted, "386.3137")