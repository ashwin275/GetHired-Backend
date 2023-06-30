from django.db import models

# Create your models here.

class PostPlans(models.Model):
    planName = models.CharField(max_length=100)
    no_of_count = models.IntegerField()
    amount = models.IntegerField()
    feature_one = models.CharField(max_length=150,blank=True)
    feature_two = models.CharField(max_length=150,blank=True)
    feature_three = models.CharField(max_length=150,blank=True)
   