from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
        )

        user.is_verified = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            password=password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, unique=True)
    mobile = models.CharField(max_length=10)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    email_token = models.CharField(max_length=250, null=True)
    is_staff = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    resume = models.FileField(blank=True, null=True)
    skills = models.CharField(max_length=40, blank=True, null=True)
    experienced = models.BooleanField(default=False)
    desired_job = models.CharField(max_length=30)
    desired_location = models.CharField(max_length=30)
    qualification = models.CharField(max_length=30)


class Experience(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    designation = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    start = models.IntegerField()
    end = models.IntegerField()
    description = models.TextField()
