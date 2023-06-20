from rest_framework.views import APIView
from users.models import Account
from users.serializers import UserInfoSerializer,UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework import status
from rest_framework.exceptions import NotFound
# Create your views here.

class AdminHomeview(APIView):
        
     def get(self,request):
         user = request.user
         print(user,'ooooooooooooooooooooo')
         if not user.is_superuser:
             return Response({'detail':'You are not an admin'},status=status.HTTP_403_FORBIDDEN)
         
         serialized_data = UserInfoSerializer(user)
         return Response(serialized_data.data)
    
    
class AdminViewUserManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Account.objects.get(id=pk)
        except Account.DoesNotExist:
            raise NotFound('User not found')

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        users = Account.objects.filter(is_seeker = True)
        UserList = UserSerializer(users, many=True)
        return Response(UserList.data)

    def delete(self, request, pk):
        try:
            user = self.get_object(pk)
            user.delete()
            return Response({'message': 'Account deleted successfully'})
        except Account.DoesNotExist:
            return Response({'message': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,pk):
        user = self.get_object(pk)

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        serializer = UserInfoSerializer(user)
        return Response({
            'status' : 400,
            'data':serializer.data

        })





class AdminViewEmployerManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        users = Account.objects.filter(is_employer=True)
        UserList = UserSerializer(users, many=True)
        return Response(UserList.data)


