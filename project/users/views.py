from rest_framework.views import APIView
from .models import Account
from .serializers import RegisterSerializer,UserInfoSerializer,UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .sendmails import send_email_verify
import uuid
from django.contrib.auth import get_user_model
from .models import Account
from .token import get_tokens
from rest_framework_simplejwt.tokens import AccessToken # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
# import jwt , datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken  # type: ignore

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
        print(request.data,'dataaaaaaaaaaaaaaaaaaaaaaa')
      
        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())

        user_profile = serializer.save()
        user_profile.email_token = token
        user_profile.is_active = True
        user_profile.save()
        send_email_verify(serializer.data['email'],token)
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
                    'message':'Account already verified',
                     'is_seeker':user.is_seeker
                }
                return Response( verify_response)
            else:
                user.is_verified = True
                user.is_active = True
                user.save()
                print(user,'........................................')
                print(user.is_seeker,'deeeeeeeeeeeeeeee')
                response_data = {
                'message': 'Email verified successfully.',
                'is_seeker':user.is_seeker
                }
                return Response(response_data)
        except:
             return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)



class LoginView(APIView):
   def post(self, request):
    email = request.data['email']
    password = request.data['password']
    role = request.data['role']

    try:
        user = Account.objects.get(email=email)
    except Account.DoesNotExist:
        raise AuthenticationFailed("User not found")

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password')

    if not user.is_active:
        raise AuthenticationFailed('You are blocked by admin')

    if not user.is_verified:
        raise AuthenticationFailed('Your account is not verified')

    # match role:
    #     case 'is_seeker':
    #         if not user.is_seeker:
    #             raise AuthenticationFailed('You are not a user')
    #     case 'is_employer':
    #         if not user.is_employer:
    #             raise AuthenticationFailed('You are not an employer')
    #     case 'is_superuser':
    #         if not user.is_superuser:
    #             raise AuthenticationFailed('You are not an admin')
    #     case _:
    #         raise AuthenticationFailed('Invalid role')

    Serialized_data = UserInfoSerializer(user)
    token = get_tokens(user)
    response = Response()
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data = {
        'userInfo': Serialized_data.data,
        'token': token,
        'message':'successfully loged',
         'status':200
    }
    return response
   
    
   def get(self,request):
        user_id = request.user
        print(user_id)
        # user = Account.objects.get(id=user_id)
        return Response({'user_id': user_id})

   

#    def get(self, request):
#         token = request.headers.get('Authorization')
#         if token.startswith('Bearer '):
#             token = token[7:]

#         if not token:
#             raise AuthenticationFailed('Unauthenticated!1212121212')
#         try:
           
#             # token = token.split(' ')[1]
#             # payload = jwt.decode(token, 'secret', algorithms=['HS256'])

#             # user = Account.objects.get(id=payload['user_id'])

#             acces_token = AccessToken(token)
#             user_id = acces_token['user_id']
#             user = Account.objects.get(id=user_id)
#             print(user,'user')
#             serializer = UserSerializer(user)
#             return Response(serializer.data)

#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticateddddd!')

#         except (jwt.DecodeError, Account.DoesNotExist):
#             raise AuthenticationFailed('Unauthenticated!')


# class UsersList(APIView):

class UserDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.auth:
            raise AuthenticationFailed('Unauthenticated!')
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        try:
            token = RefreshToken(token)
            token.blacklist()
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        return Response({'detail': 'Logout successful'})



    
