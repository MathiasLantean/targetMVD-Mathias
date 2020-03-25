from django.contrib.gis.db import models
from profile.models import User


class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    radius = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.PointField()
