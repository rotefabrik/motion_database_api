from django.contrib.gis.db import models


class Convention(models.Model):
    label = models.CharField(max_length=64, unique=True)
    slot = models.IntegerField()
    year = models.DateField()

    class Meta:
        unique_together = ('year', 'slot')


class Section(models.Model):
    name = models.CharField(max_length=128, unique=True)
