from rest_framework import serializers,validators
from users.models import Account,UserProfile








class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = ['id','first_name','email','is_superuser','is_employer','is_seeker','is_active']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password','email_token')




