from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import EmployerInfoSerializer,EmployerEditSerializer,AddPostSerializer
from rest_framework.permissions import IsAuthenticated
from .models import RecruitersProfile,JobPost
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



class EmployersHomeView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self,request):
        user = request.user

        if not user.is_employer:
            return Response({'detail':'You are not an employer'},status=status.HTTP_403_FORBIDDEN)

        serialized_data = EmployerInfoSerializer(user)
        return Response( serialized_data.data)
    




class EmployerEditView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        try:
            user_profile = RecruitersProfile.objects.get(user=user)
            print(user_profile, 'found')
        except RecruitersProfile.DoesNotExist:
            user_profile = RecruitersProfile.objects.create(user=user)
            print(user_profile, 'created')

        serialized_data = EmployerEditSerializer(user_profile,data=request.data,partial = True)
        if serialized_data.is_valid():
            serialized_data.save(raise_exception=True)
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors)
        

class AddPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company = RecruitersProfile.objects.get(user = request.user)
        if company.post_balance == 0:
            return Response({"message":'No posts available for your account please buy posts'},status=status.HTTP_402_PAYMENT_REQUIRED)
        serializer = AddPostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        company.post_balance -= 1
        company.save()
        return Response({"data": serializer.data, "balance_post": company.post_balance}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
            try:
                job_post = JobPost.objects.get(id=pk)
                print(request.data,'111111111111111')
                serializer = AddPostSerializer(job_post, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({'message': 'Post edited successfully','data':serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except JobPost.DoesNotExist:
                return Response({"message": 'Not found'}, status=status.HTTP_404_NOT_FOUND)