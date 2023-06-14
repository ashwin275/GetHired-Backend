from django.db import models
from users.models import Account
# Create your models here.


class RecruitersProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True)
    recruiter_bio = models.TextField(max_length=255,blank=True)
    location = models.CharField(max_length=40)
    company_name = models.CharField(max_length=40)
    company_website = models.URLField(null=True,default=None)
    company_email = models.EmailField(max_length=30)
    company_mobile = models.CharField(max_length=30)
    company_address_line1 = models.CharField(max_length=50)
    company_address_line2 = models.CharField(max_length=50)
    description = models.TextField()
    post_balance = models.IntegerField(default=0,null=True)