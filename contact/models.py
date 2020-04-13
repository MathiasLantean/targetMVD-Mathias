from django.db import models


class Information(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    detail = models.TextField(blank=True)
