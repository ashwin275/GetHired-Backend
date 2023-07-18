from django.db import models
from users.models import Account
# Create your models here.


class RecruitersProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True,null=True,default=None)
    recruiter_bio = models.TextField(max_length=255,blank=True)
    location = models.CharField(max_length=40)
    company_name = models.CharField(max_length=40)
    company_website = models.URLField(null=True,default=None)
    company_email = models.EmailField(max_length=30)
    company_mobile = models.CharField(max_length=30)
    company_address_line1 = models.CharField(max_length=50)
    company_address_line2 = models.CharField(max_length=50)
    description = models.TextField()
    post_balance = models.IntegerField(default=2,null=True)



class JobPost(models.Model):
    company = models.ForeignKey(RecruitersProfile,on_delete=models.CASCADE)
    desgination = models.CharField(blank=True)
    skills = models.TextField(blank=True)
    vaccancies = models.IntegerField(blank=True,null=True)
    location = models.TextField(blank=True)
    Type = models.CharField(blank=True)
    workmode = models.CharField(blank=True)
    experience_from = models.CharField(blank=True)
    experience_to = models.CharField(blank=True)
    job_description = models.TextField()
    criteria = models.CharField(blank=True)
    payscale_from = models.CharField(blank=True)
    payscale_to = models.CharField(blank=True)
    applicants = models.IntegerField(default=0)
    hired_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True) 



class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    order_payment_id = models.CharField(max_length=300)