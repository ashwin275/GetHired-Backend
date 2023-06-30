from rest_framework import serializers,validators
from users.models import Account,UserProfile
from .models import PostPlans








class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ['id','first_name','email','is_superuser','is_employer','is_seeker','is_active']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password','email_token')

class PostPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPlans
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance,validated_data)
        instance.save()
        return instance




