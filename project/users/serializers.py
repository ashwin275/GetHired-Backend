from rest_framework import serializers,validators
from .models import Account,UserProfile




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
         model = Account
         
         fields = ["id","first_name", "last_name", "email", "phone_number","password","is_seeker","is_recruiter","is_active"]

         extra_kwargs = {
            'password':{'write_only':True},
             'email':{
                'required':True,
                'allow_blank':False,
                'validators':[
                    validators.UniqueValidator(
                        Account.objects.all(),'A user with this email already exists'
                    )
                ]
            }
        }