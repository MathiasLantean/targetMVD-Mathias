from django.db import models
from django.db.models import UniqueConstraint


class Information(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    detail = models.TextField(blank=True)


class Chat(models.Model):
    target_one = models.ForeignKey('target.Target', related_name="chat_one_set", on_delete=models.CASCADE)
    target_two = models.ForeignKey('target.Target', related_name="chat_two_set", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.target_one.user} {self.target_two.user}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['target_one', 'target_two'], name='unique_chat_between_targets_one_two'),
            UniqueConstraint(fields=['target_two', 'target_one'], name='unique_chat_between_targets_two_one'),
        ]
