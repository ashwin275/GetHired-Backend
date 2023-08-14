from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .serializer import EmployerInfoSerializer, EmployerEditSerializer, AddPostSerializer, PostsSerializers, PostDetailSerializer, JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import RecruitersProfile, JobPost, Payment, JobApplication
from users.models import UserProfile,Account
from django.views.decorators.csrf import csrf_exempt
from adminhome.serializers import PostPlanSerializer
from adminhome.models import PostPlans
from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination
from users.permission import IsRecruiters
from users.sendmails import send_employer_action_mail
# Create your views here.


class EmployersHomeView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]

    def get(self, request):
        user = request.user

        try:
            Recruiter_profile = RecruitersProfile.objects.get(user=user)
            print('recruiter profile found')
        except:
            Recruiter_profile = RecruitersProfile.objects.create(user=user)
            print('profile created')

        serialized_data = EmployerInfoSerializer(Recruiter_profile)
        return Response(serialized_data.data)


class EmployerEditView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]

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

        serialized_data = EmployerEditSerializer(
            user_profile, data=request.data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save(raise_exception=True)
            return Response({'data': serialized_data.data, 'message': 'profile has been succesfully edited'})
        else:
            return Response(serialized_data.errors)


class AddPostView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]

    def get(self, request):

        try:
            Recruiter = RecruitersProfile.objects.get(user=request.user)
            job_post = JobPost.objects.filter(
                company=Recruiter).order_by('-id')
            serializer = PostsSerializers(job_post, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except RecruitersProfile.DoesNotExist:
            return Response("Recruiter profile does not exist.", status=status.HTTP_404_NOT_FOUND)
        except JobPost.DoesNotExist:
            return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        company = RecruitersProfile.objects.get(user=request.user)
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        if company.post_balance == 0:
            print(company.post_balance, 'post balance')
            return Response({"message": 'No posts available for your account please buy posts'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        serializer = AddPostSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        company.post_balance -= 1
        company.save()
        return Response({"data": serializer.data, "balance_post": company.post_balance, "message": 'Post has been successfully added!'}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job_post = JobPost.objects.get(id=pk)
            print(request.data, '111111111111111')
            serializer = AddPostSerializer(
                job_post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'Post edited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobPost.DoesNotExist:
            return Response({"message": 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            post = JobPost.objects.get(id=pk)
            post.delete()
            return Response({'message': 'post deleted succesfully'}, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]

    def get(self, request, pk):
        try:
            post = JobPost.objects.get(id=pk)
            serialized_data = PostDetailSerializer(post)
            return Response({'data': serialized_data.data}, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response("Job post does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyPostPlanview(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]

    def get(self, request):

        try:
            post = PostPlans.objects.all()
            serializer = PostPlanSerializer(post, many=True)
            return Response({'data': serializer.data})
        except APIException as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if not request.data:
            return Response({'error': 'No data provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        plan_id = request.data.get('plan_id')
        order_id = request.data.get('order_id')

        amount = request.data.get('amount')

        try:
            post = PostPlans.objects.get(id=plan_id)
            if amount:
                print(amount, post.amount)
                if float(amount) != float(post.amount):
                    return Response({
                        'error': 'amount doesnot match'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'provide amount'
                }, status=status.HTTP_400_BAD_REQUEST)
        except PostPlans.DoesNotExist:
            return Response({
                'error': 'PostPlan doesnot exist'
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            payment = Payment.objects.create(
                user=request.user,
                amount=post.amount,
                is_paid=True,
                order_payment_id=order_id
            )
            payment.save()
            user_account = RecruitersProfile.objects.get(user=request.user)
            user_account.post_balance += post.no_of_count
            user_account.save()
            return Response({
                'message': 'payment succes',
                'post_balance': user_account.post_balance
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApplicantsListApiView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiters]
    pagination_class = LimitOffsetPagination

    def get(self, request, pk=None):

        try:

            if not pk:
                return Response({
                    'error': 'provide a valid id'
                }, status=status.HTTP_400_BAD_REQUEST)
            try:
                jobPost = JobPost.objects.get(id=pk)
            except JobPost.DoesNotExist:
                return Response({
                    'error':  'JobPost not found'
                }, status=status.HTTP_404_NOT_FOUND)
            applicants = JobApplication.objects.filter(job=jobPost.id).order_by('-id')
            paginator = self.pagination_class()
            paginated_applicants = paginator.paginate_queryset(
                applicants, request)
            serializer = JobApplicationSerializer(
                paginated_applicants, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:

            try:

                application = JobApplication.objects.get(id=pk)

            except JobApplication.DoesNotExist:
                return Response({
                    'error': 'job application doesnot found'
                }, status=status.HTTP_404_NOT_FOUND)

            match application.status:
                case 'applied':
                    application.status = 'shortlisted'
                    user_email = application.user.user.email
                    application_designation = application.job.desgination
                    company = application.recruiter.company_name
                   
                    message = f'Congratulations! We are excited to inform you that your job application for {application_designation} has been shortlisted by  {company}. Your qualifications and experience have impressed them, and you are one step closer to the next stages of the selection process. Keep up the good work and prepare yourself for the upcoming rounds. Thank you for choosing our platform, and we wish you the best of luck in the further evaluation!'
                    subject = 'Get-Hired Application Shortlisted'
                    send_employer_action_mail(user_email,message,subject)
                case 'shortlisted':
                    application.status = 'intervied'
                    
                case 'intervied':
                    application.status = 'selected'
                    job = JobPost.objects.get(id=application.job.id)
                    job.hired_count +=1
                    job.save()

            application.save()
            return Response({'message': 'succes'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RejectApplicationApiView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]

    def patch(self,request,pk):
        try:

            try:

                application = JobApplication.objects.get(id=pk)

            except JobApplication.DoesNotExist:
                return Response({
                    'error': 'job application doesnot found'
                }, status=status.HTTP_404_NOT_FOUND)
         
            application.status = 'rejected'
            application.save()
            subject = 'Get-Hired Application rejected'
            user_email = application.user.user.email
            application_designation = application.job.desgination
            company = application.recruiter.company_name
                   
           
            message = f'We regret to inform you that your job application  for {application_designation}has been rejected by {company}. We appreciate your interest and effort in applying for the position. Please dont be discouraged, as there are many other opportunities out there. Keep refining your skills and exploring new possibilities. Thank you for choosing our platform, and we wish you success in your job search!'
            print('called function')
            hello = send_employer_action_mail(user_email,message,subject)
            print('return',hello)
            return Response({
                'message':'succesfully rejected'
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ResumeDownloadedApiView(APIView):
    permission_classes = [IsAuthenticated,IsRecruiters]

    def post(self,request,pk):
        print(pk)
        try:
            try:
                application = JobApplication.objects.get(id=pk)
            except JobApplication.DoesNotExist:
                return Response({
                    'error':'application doesnot exist'
                },status=status.HTTP_404_NOT_FOUND)
            if application.is_downloaded:
                return Response({
                    'message':'already viewed by employer'
                })
            user_email = application.user.user.email
            application_designation = application.job.desgination
            company = application.recruiter.company_name
            subject = 'Get-Hired resume downloaded'
            message = f'Congratulations! We are thrilled to inform you that your resume has been downloaded by {company} for the application to the position of {application_designation}. This is an exciting opportunity, and we wish you the best of luck in the selection process. We believe your skills and experience make you a strong candidate, and we look forward to seeing your continued success. Should you have any questions or require further information, please dont hesitate to reach out. Thank you for choosing our platform, and we hope this leads you to your dream job!'
            send_employer_action_mail(user_email,message,subject)
            application.is_downloaded = True
            application.save()

            return Response({
                'message':'email succesfully send'
            },status=status.HTTP_200_OK)



        except Exception as e:
            return Response({
                'error':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class UserResumeDownloadApiView(APIView):
    permission_classes =[IsAuthenticated,IsRecruiters]
    def get(self, request, pk, format=None):
        try:
            try:
               user = Account.objects.get(id=pk)
            except Account.DoesNotExist:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            user_profile = UserProfile.objects.get(user=user)
            print(user_profile)
            if user_profile.resume:

                resume_file = user_profile.resume.path
                print('path',resume_file)
                with open(resume_file, 'rb') as resume:
                    response = HttpResponse(resume.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{user.email}_resume.pdf"'
                    return response
            else:
                return Response({'detail': 'User has no resume'}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
