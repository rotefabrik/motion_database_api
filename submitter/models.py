from django.contrib.gis.db import models


class Submitter(models.Model):
    name = models.CharField(max_length=128)
