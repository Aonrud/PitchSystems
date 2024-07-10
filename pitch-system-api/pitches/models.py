from django.db import models


class Interval(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cents = models.DecimalField(max_digits=10, decimal_places=4)
    ratio_enumerator = models.IntegerField(null=True,blank=True)
    ratio_denominator = models.IntegerField(null=True,blank=True)


class Scale(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    intervals = models.ManyToManyField(Interval)
