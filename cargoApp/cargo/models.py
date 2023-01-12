from django.db import models

# Create your models here.

class CargoInfo(models.Model):

    vessel_name = models.CharField(max_length=244, null=False, blank=False)
    short_name = models.CharField(max_length=244, null=False, blank=False)
    vessel_type = models.CharField(max_length=244, null=False, blank=False)
    built = models.IntegerField()
    gt = models.IntegerField()
    dwt = models.IntegerField()
    size = models.CharField(max_length=244, null=False, blank=False)
    draft = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=16)

    class Meta:
        ordering = ['id']




