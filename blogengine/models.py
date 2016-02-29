from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()