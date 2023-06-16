from rest_framework.views import APIView
from .models import Account
from .serializers import RegisterSerializer,UserInfoSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .sendmails import send_email_verify
import uuid
from django.contrib.auth import get_user_model
from .models import Account
from django.views.decorators.csrf import csrf_exempt



# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
# from rest_framework_simplejwt.views import TokenObtainPairView            # type: ignore
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username 
#         # ...

#         return token
    
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self,request):
      
        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())

        user_profile = serializer.save()
        user_profile.email_token = token
        user_profile.save()
        # send_email_verify(serializer.data['email'],token)
        response = Response()
        response.data = {
         'message': f"Account successfully created for {serializer.data['first_name']}",
         'message_email':f"Email verification required ",
         'Userinfo':serializer.data
              }
        return response
    
    def get(self,request,token):
        # User = get_user_model()
        try:
            user = Account.objects.get(email_token=token)
            if user.is_verified == True:
                verify_response = {
                    'message':'Account already verified'
                }
                return Response( verify_response)
            else:
                user.is_verified = True
                user.is_active = True
                user.save()
                print(user,'........................................')
                response_data = {
                'message': 'Email verified successfully.',
                'is_seeker':user.is_seeker
                }
                return Response(response_data)
        except:
             return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)



class LoginView(APIView):
    @csrf_exempt
    def post(self,request):
        email = request.data['email']
        password = request.data['password']


        try:
            user = Account.objects.get(email = email)
        except Account.DoesNotExist:
            raise AuthenticationFailed("User not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorect password')
        
        if not user.is_active:
            raise AuthenticationFailed('you are blocked by admin')   
        
        Serialized_data = UserInfoSerializer(user)
        response = Response()

        response.data = {
            'userInfo':Serialized_data.data
        }


        return response
