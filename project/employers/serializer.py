from rest_framework import serializers
from .models import RecruitersProfile , JobPost ,JobApplication
from users.models import Account


class EmployerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitersProfile
        fields = '__all__'



class EmployerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitersProfile
        fields = '__all__'


        def update(self,instance,vaidated_data):
            image = vaidated_data.pop('profile_picture',None)
            instance = super().update(instance,vaidated_data)


            if image:
                instance.image = image
                instance.save()
                return instance
            


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ['company']

    def create(self, validated_data):
        user = self.context['request'].user
        company = RecruitersProfile.objects.get(user=user)

     
        validated_data['company'] = company
        validated_data['is_active'] = True
        instance = super().create(validated_data)
        

        return instance
    

    def update(self, instance, validated_data):
        instance = super().update(instance,validated_data)
        instance.save()
        return instance


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id','desgination','skills','location','is_active','Type','workmode']


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"



class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"