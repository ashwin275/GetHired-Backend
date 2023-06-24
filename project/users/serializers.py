from rest_framework import serializers,validators
from .models import Account,UserProfile
from employers.models import JobPost



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


class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

        fields = '__all__'


    
    def update(self, instance, validated_data):
        profile = validated_data.pop('profile_picture',None)
        resume = validated_data.pop('resume',None)
        instance = super().update(instance, validated_data)

        if profile:
            instance.profile_picture = profile

        if resume:
            instance.resume = resume

        instance.save()
        return instance


class jobpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        exclude = ('applicants','hired_count','is_active')