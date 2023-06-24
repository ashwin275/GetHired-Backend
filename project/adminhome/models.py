from django.db import models

# Create your models here.

class PostPlans(models.Model):
    planName = models.CharField(max_length=100)
    no_of_count = models.IntegerField()
    amount = models.IntegerField()