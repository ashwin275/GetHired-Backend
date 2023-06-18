from rest_framework import serializers,validators
from .models import Account,UserProfile




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
         model = Account
         
         fields = ["id","first_name", "last_name", "email", "mobile","password","is_seeker","is_employer",]

         extra_kwargs = {
            'password':{'write_only':True},
             'email':{
                'required':True,
                'allow_blank':False,
                'validators':[
                    validators.UniqueValidator(
                        Account.objects.all(),'A user with this email already exists please try with other one'
                    )
                ]
            }
        }
         
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ['id','first_name','email','is_superuser','is_employer','is_seeker']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password','email_token')