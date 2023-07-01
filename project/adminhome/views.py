from rest_framework.views import APIView
from users.models import Account
from .models import PostPlans
from users.serializers import UserInfoSerializer,UserSerializer
from .serializers import PostPlanSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permission import IsSuperuser
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException ,NotFound
# Create your views here.

class AdminHomeview(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request):
         user = request.user
         print(user,'ooooooooooooooooooooo')
         if not user.is_superuser:
             return Response({'detail':'You are not an admin'},status=status.HTTP_403_FORBIDDEN)
         
         serialized_data = UserInfoSerializer(user)
         return Response(serialized_data.data)
    
    
class AdminViewUserManage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

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
    permission_classes = [IsAuthenticated, IsSuperuser]

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({'detail': 'You are not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        users = Account.objects.filter(is_employer=True)
        UserList = UserSerializer(users, many=True)
        return Response(UserList.data)




class AddPostPlanView(APIView):
    permission_classes = [IsAuthenticated, IsSuperuser]

    def post(self, request):
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

        
        
        serializer = PostPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data,
            'message': 'New Plan created successfully',
        }, status=status.HTTP_201_CREATED)
  


    
       
        
    def get(self,request,pk = None):

        if pk is not None:
            try:
                post = PostPlans.objects.get(id=pk)

                serializer = PostPlanSerializer(post)
                return Response({'data':serializer.data})
            except APIException as e :
                return Response({'detail':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            try:
                post = PostPlans.objects.all().order_by('-id')
                serializer = PostPlanSerializer(post, many=True)
                return Response({'data': serializer.data})
            except APIException as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    def patch(self, request, pk):
        if not request.data:
             return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = PostPlans.objects.get(id=pk)
        except PostPlans.DoesNotExist:
            raise NotFound("Post plan not found.")

        serializer = PostPlanSerializer(post, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'data': serializer.data,"message":' Updated succesfully'},status=status.HTTP_200_OK)

    def delete(self,request,pk):
        try:
            post = PostPlans.objects.get(id=pk)
            post.delete()
            return Response({'message':"Plan has been deleted succesfully"},status=status.HTTP_200_OK)
        except PostPlans.DoesNotExist:
            raise NotFound("post plan not found")
        except APIException as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



