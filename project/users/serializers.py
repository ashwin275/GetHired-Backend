from rest_framework import serializers,validators
from .models import Account,UserProfile,Experience
from employers.models import JobPost,JobApplication



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
    user = serializers.SerializerMethodField()
    
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile

        fields = '__all__'

    def get_user(self,obj):
        return obj.user.first_name
    def get_last_name (self,obj):
        return obj.user.last_name
    def get_email(self,obj):
        return obj.user.email
    
    def get_mobile(self,obj):
        return obj.user.mobile
    
    def update(self, instance, validated_data):
        
        
        
        profile = validated_data.pop('profile_picture',None)
        resume = validated_data.pop('resume',None)
        instance = super().update(instance, validated_data)
        print('called for updation')
        if profile:
            instance.profile_picture = profile

        if resume:
            instance.resume = resume

        instance.save()
        return instance

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ['user']
     

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def validate(self, data):
        start = data['start']
        end = data['end']

        if start >= end:
            raise serializers.ValidationError("Start date must be before the end date.")
        
        user = self.context['request'].user
        overlapping_experiences = Experience.objects.filter(
            user=user,
            start__lt=end,
            end__gt=start,
        )

        if self.instance:
            
            overlapping_experiences = overlapping_experiences.exclude(pk=self.instance.pk)

        if overlapping_experiences.exists():
            raise serializers.ValidationError("Cannot add another experience with overlapping dates. Choose another dates")

        return data
class jobpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        exclude = ('applicants','hired_count','is_active')


class JobListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    
    profile_picture = serializers.SerializerMethodField()
    

    class Meta:
        model = JobPost
        fields = ['id','desgination', 'location', 'company','profile_picture']
        
    def get_company(self, obj):
        return obj.company.company_name

    # def get_company_email(self, obj):
    #     return obj.company.company_email
    def get_profile_picture(self, obj):
        return obj.company.profile_picture.url
    


class JobDetailSerialzer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    company_email = serializers.SerializerMethodField()
    company_mobile = serializers.SerializerMethodField()
    company_website = serializers.SerializerMethodField()
    class Meta:
        model = JobPost
        exclude = ['hired_count']


    def get_company(self, obj):
        return obj.company.company_name
    
    def get_profile_picture(self, obj):
        return obj.company.profile_picture.url
    
    def get_company_email(self,obj):
        return obj.company.company_email
    def get_company_mobile(self,obj):
        return obj.company.company_mobile
    def get_company_website(self,obj):
        return obj.company.company_website


class JobApplicationSerializers(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    JobPostId = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    # profile_picture = serializers.SerializerMethodField()
    recruiter = serializers.SerializerMethodField()
    Emp_ID = serializers.SerializerMethodField()
    class Meta:
        model = JobApplication
        exclude = ['user']
    def get_JobPostId(self,obj):
        return obj.job.id
    def get_recruiter(self,obj):
        return obj.recruiter.company_name
    
    def get_job(self, obj):
        return obj.job.desgination

    def get_Emp_ID(self,obj):
        return obj.recruiter.user.id
    
    # def get_profile_picture(self,obj):
    #     return obj.recruiter.profile_picture

    
    def get_location(self,obj):
        return obj.job.location
    
    # def get_company_name(self,obj):
    #     return obj.recruiter.company_name


class JobApplicationChatSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    job_id = serializers.SerializerMethodField()
    recruiter = serializers.SerializerMethodField()
    emp_id = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        exclude = ['user','created','status','modified','is_downloaded']


    def get_job(self, obj):
        return obj.job.desgination
    def get_recruiter(self,obj):
        return obj.recruiter.company_name
    
    def get_job_id(self,obj):
        return obj.job.id
    def get_emp_id (self,obj):
        return obj.recruiter.user.id
    
   