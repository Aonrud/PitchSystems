from django.db import models


class Interval(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cents = models.DecimalField(max_digits=10, decimal_places=4)
    ratio_numerator = models.IntegerField(null=True, blank=True)
    ratio_denominator = models.IntegerField(null=True, blank=True)

    ordering = ["name"]
    search_fields = ["name"]

    def __str__(self):
        return self.name


class Scale(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    intervals = models.ManyToManyField(Interval)

    ordering = ["name"]
    autocomplete_fields = ["intervals"]

    def __str__(self):
        return self.name
