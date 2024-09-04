from django.db import models


class AbstractBaseModel(models.Model):
    """
    The base model includes shared fields for other models
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    ordering = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Nomenclature(AbstractBaseModel):
    """
    A definition of a musical term.
    """


class System(AbstractBaseModel):
    """
    Model for a system of pitches or tuning
    """


class Interval(AbstractBaseModel):
    """
    Model for an interval
    """

    cents = models.DecimalField(max_digits=10, decimal_places=4)
    ratio_numerator = models.IntegerField(null=True, blank=True)
    ratio_denominator = models.IntegerField(null=True, blank=True)

    ordering = ["cents"]

    def __str__(self):
        return str(self.cents)


class IntervalName(AbstractBaseModel):
    """
    Model for an interval name, which can be specific to a system.
    """

    system = models.ForeignKey(System, null=True, on_delete=models.CASCADE)
    interval = models.ForeignKey(
        Interval, related_name="additional_names", on_delete=models.CASCADE
    )
    # Specifies the name applies when the interval is used at a particular scale degree – e.g. augmented 2nd vs. minor 3rd  
    degree = models.IntegerField(null=True, blank=True)


class Scale(AbstractBaseModel):
    """
    Model for a scale or set of intervals
    """

    intervals = models.ManyToManyField(
        Interval,
        through="IntervalRole",
        through_fields=("scale", "interval")
    )
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    root = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    ordering = ["name"]
    autocomplete_fields = ["intervals"]

    def __str__(self):
        return self.name

class IntervalRole(models.Model):
    """
    Model for information about the role of an interval in a scale.
    """
    role = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    
