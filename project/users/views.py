from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .sendmails import send_email_verify
import uuid
from django.contrib.auth import get_user_model
from .models import Account


class RegisterView(APIView):
    def post(self,request):
        print(request.data,'111111111111111111111111')
        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())

        user_profile = serializer.save()
        user_profile.email_token = token
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
            if user.is_verified:
                return Response({
                    'message':'Account already verified'
                   })
            user.is_verified = True
            user.save()
            print(user,'........................................')
            response_data = {
            'message': 'Email verified successfully.',
            }
            return Response(response_data)
        except:
             return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

