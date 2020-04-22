from django.contrib.gis.db import models
from django.db.models import F
from easy_thumbnails.fields import ThumbnailerImageField
from profile.models import User


class Topic(models.Model):
    title = models.CharField(max_length=255)
    photo = ThumbnailerImageField(upload_to='topics', blank=True)

    def __str__(self):
        return f'{self.pk} - {self.title}'


class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    radius = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.PointField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=1, blank=False)

    def __str__(self):
        return f'{self.pk} - {self.user.email}, {self.title}'

    def get_matches(self):
        return Target.objects.filter(
            location__distance_lte=(self.location, self.radius + F('radius')),
            topic=self.topic,
        ).exclude(user=self.user)
