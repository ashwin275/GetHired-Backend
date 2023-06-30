from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import EmployerInfoSerializer,EmployerEditSerializer,AddPostSerializer,PostsSerializers,PostDetailSerializer
from rest_framework.permissions import IsAuthenticated
from .models import RecruitersProfile,JobPost
from django.views.decorators.csrf import csrf_exempt
from users.permission import IsRecruiters
# Create your views here.



class EmployersHomeView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]
   
    def get(self,request):
        user = request.user

        try:
            Recruiter_profile = RecruitersProfile.objects.get(user = user)
            print('recruiter profile found')
        except Recruiter_profile.DoesNotExist:
            Recruiter_profile = RecruitersProfile.objects.create(user = user)
            print('profile created')

        serialized_data = EmployerInfoSerializer(Recruiter_profile)
        return Response( serialized_data.data)
    

class EmployerEditView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]

    def patch(self, request):
        user = request.user
        if not request.data:
             return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            user_profile = RecruitersProfile.objects.get(user=user)
            print(user_profile, 'found')
        except RecruitersProfile.DoesNotExist:
            user_profile = RecruitersProfile.objects.create(user=user)
            print(user_profile, 'created')

        serialized_data = EmployerEditSerializer(user_profile,data=request.data,partial = True)
        if serialized_data.is_valid():
            serialized_data.save(raise_exception=True)
            return Response({'data':serialized_data.data,'message':'profile has been succesfully edited'})
        else:
            return Response(serialized_data.errors)
        

class AddPostView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]

    

    def get(self, request):
        try:
            Recruiter = RecruitersProfile.objects.get(user=request.user)
            job_post = JobPost.objects.filter(company=Recruiter).order_by('-id')
            serializer = PostsSerializers(job_post, many=True)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        except RecruitersProfile.DoesNotExist:
            return Response("Recruiter profile does not exist.", status=status.HTTP_404_NOT_FOUND)
        except JobPost.DoesNotExist:
            return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        company = RecruitersProfile.objects.get(user = request.user)
        if not request.data:
             return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        if company.post_balance == 0:
            print(company.post_balance,'post balance')
            return Response({"message":'No posts available for your account please buy posts'},status=status.HTTP_402_PAYMENT_REQUIRED)
        serializer = AddPostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        company.post_balance -= 1
        company.save()
        return Response({"data": serializer.data, "balance_post": company.post_balance,"message":'Post has been successfully added!'}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
            if not request.data:
             return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
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
            
    def delete(self, request, pk):
        try:
            post = JobPost.objects.get(id=pk)
            post.delete()
            return Response({'message':'post deleted succesfully'},status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
                 return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostDetailView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]
    def get(self, request, pk):
        try:
            post = JobPost.objects.get(id=pk)
            serialized_data = PostDetailSerializer(post)
            return Response({'data': serialized_data.data}, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
