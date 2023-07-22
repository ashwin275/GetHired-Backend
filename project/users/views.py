from rest_framework.views import APIView
from .models import Account
from .serializers import RegisterSerializer, UserInfoSerializer, UserSerializer, JobSeekerSerializer, jobpostSerializer, JobListSerializer, JobDetailSerialzer, ExperienceSerializer, JobApplicationSerializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .sendmails import send_email_verify
import uuid
from django.contrib.auth import get_user_model, login
from .models import Account, UserProfile, Experience
from employers.models import RecruitersProfile, JobApplication
from .token import get_tokens
from rest_framework_simplejwt.tokens import AccessToken  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
# import jwt , datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken  # type: ignore
from django.utils import timezone
from .permission import IsSeeker
from employers.models import JobPost
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import APIException
from django.db.models import Q

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
    def post(self, request):
        print(request.data, 'dataaaaaaaaaaaaaaaaaaaaaaa')

        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())

        user_profile = serializer.save()
        user_profile.email_token = token
        user_profile.is_active = True
        user_profile.save()
        send_email_verify(serializer.data['email'], token)
        response = Response()
        response.data = {
            'message': f"Account successfully created for {serializer.data['first_name']}",
            'message_email': f"Email verification required ",
            'Userinfo': serializer.data
        }
        return response

    def get(self, request, token):
        # User = get_user_model()
        try:
            user = Account.objects.get(email_token=token)
            if user.is_verified == True:
                verify_response = {
                    'message': 'Account already verified',
                    'is_seeker': user.is_seeker
                }
                return Response(verify_response)
            else:
                user.is_verified = True
                user.is_active = True
                user.save()
                print(user, '........................................')
                print(user.is_seeker, 'deeeeeeeeeeeeeeee')
                response_data = {
                    'message': 'Email verified successfully.',
                    'is_seeker': user.is_seeker
                }
                return Response(response_data)
        except:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        if not request.data:
            return Response({'error': 'No data provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            role = request.data.get('role')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        if not user.is_active:
            raise AuthenticationFailed('Your account is blocked')

        if not user.is_verified:
            raise AuthenticationFailed('Your account is not verified')

        match role:
            case 'is_seeker':
                if not user.is_seeker:
                    raise AuthenticationFailed('You are not an user')
            case 'is_employer':
                if not user.is_employer:
                    raise AuthenticationFailed('You are not an employer')
            case 'is_superuser':
                if not user.is_superuser:
                    raise AuthenticationFailed('You are not an admin')
            case _:
                raise AuthenticationFailed('Invalid role')
        user.last_login = timezone.now()
        print(timezone.now())
        user.save()
        print(user.last_login)
        Serialized_data = UserInfoSerializer(user)
        token = get_tokens(user)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'userInfo': Serialized_data.data,
            'token': token,
            'message': 'successfully loged',
            'status': 200
        }
        return response

    def get(self, request):
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


class UserHomeView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def get(self, request):
        user = request.user

        try:
            user_profile = UserProfile.objects.get(user=user)
            print('user profile found')
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user)
            print('profile created')

        serialized_data = JobSeekerSerializer(user_profile)
        pofile_completness = user_profile.get_completeness()

        return Response({'data': serialized_data.data,
                         'profile_completness': round(pofile_completness, 1),
                         'message': 'success'}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            try:
                email = request.data.get('email', None)

                if email:
                    try:
                        existing_user = Account.objects.get(email=email)
                        if existing_user != request.user:

                            error_message = "Email is already in use by another user."
                            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                    except UserProfile.DoesNotExist:

                        pass
            except:
                pass
            try:
                user_instance = request.user
                user_instance.first_name = request.data.get(
                    'first_name', user_instance.first_name)
                user_instance.last_name = request.data.get(
                    'last_name', user_instance.last_name)
                user_instance.email = request.data.get(
                    'email', user_instance.email)
                user_instance.mobile = request.data.get(
                    'mobile', user_instance.mobile)
                user_instance.save()

            except Exception as e:
                error_message = str(e)
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user_profile = UserProfile.objects.get(user=user)
                print('user profile found')
            except UserProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serialized_data = JobSeekerSerializer(
                user_profile, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save(raise_exception=True)
                userInfo_serializer = UserInfoSerializer(request.user)
                return Response({'data': serialized_data.data,
                                 'userInfo': userInfo_serializer.data,
                                 'message': 'updated succesfully'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serialized_data.errors)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExperienceApiView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def get(self, request):
        try:

            userExperience = Experience.objects.filter(user=request.user)
            if not userExperience:
                return Response({'error': 'No experiences found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ExperienceSerializer(userExperience, many=True)
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Experience.DoesNotExist:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = ExperienceSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                userpofile = UserProfile.objects.get(user=request.user)
                userpofile.experienced = True
                userpofile.save()
                return Response({
                    'message': 'Experience  added'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.error}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            try:
                experience = Experience.objects.get(id=pk)
            except Experience.DoesNotExist:
                return Response({
                    'error': 'not found'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ExperienceSerializer(
                experience, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'message': 'updated succesfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            experience = Experience.objects.get(id=pk)
        except Experience.DoesNotExist:
            return Response({
                'error': 'not found'
            }, status=status.HTTP_404_NOT_FOUND)

        experience.delete()
        return Response({
            'message': 'succesfully removed'
        }, status=status.HTTP_200_OK)


class ViewJobPosts(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get(self, request):
        try:
            userProfile = UserProfile.objects.get(user = request.user)
            desired_job = userProfile.desired_job [:3]
        
            jobs = JobPost.objects.filter(Q(desgination__icontains=userProfile.desired_job)|Q(desgination__icontains = desired_job ) ).order_by('-id')
            print(jobs)
            paginator = self.pagination_class()
            paginated_jobs = paginator.paginate_queryset(jobs, request)
            serializer = JobListSerializer(paginated_jobs, many=True)
            print('data called')
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            raise APIException('Error retrieving job posts: {}'.format(str(e)))


class SearchJobPostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

          

            search_query_company = request.GET.get('company')
            search_query_job = request.GET.get('job')
            search_query_skills = request.GET.get('skills')
            search_query_location = request.GET.get('location')

            if not (search_query_company or search_query_job or search_query_skills or search_query_location):
                return Response({'error': 'Provide at least one valid search query.'},
                                status=status.HTTP_400_BAD_REQUEST)

            filters = Q()

            if search_query_company:
                filters &=  Q(company__company_name__icontains=search_query_company) 

            if search_query_job:
                filters &= Q(desgination__icontains=search_query_job)
            
            if search_query_skills:
                filters &= Q(skills__icontains=search_query_skills)
            
            if search_query_location :
                filters &= Q(location__icontains = search_query_location )

           
            print(filters)

            jobs = JobPost.objects.filter(filters).order_by('-id')
            serializer = JobListSerializer(jobs, many=True)
            return Response({
                'data': serializer.data
            })

        except Exception as e:
            raise APIException('Error retrieving job posts: {}'.format(str(e)))


class ViewJobDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        

        try:
            try:
                jobs = JobPost.objects.get(id=pk)
            except:
                return Response({'error': 'Job Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = JobDetailSerialzer(jobs,)

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            raise APIException('Error retrieving job posts: {}'.format(str(e)))


class jobApplyApiView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def post(self, request, pk):
        try:

            try:
                Job = JobPost.objects.get(id=pk)
            except JobPost.DoesNotExist:
                return Response({
                    'error', 'job doesnot exist'
                }, status=status.HTTP_400_BAD_REQUEST)

            userProfile = UserProfile.objects.get(user=request.user)
            recruiters = RecruitersProfile.objects.get(user=Job.company.user)
            print(recruiters)
            try:
                jobappied = JobApplication.objects.get(
                    user=userProfile, job=Job, recruiter=recruiters)
                if jobappied:
                    return Response({
                        'error': 'Job Already Applied'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            job_application = JobApplication.objects.create(
                user=userProfile,
                recruiter=recruiters,
                job=Job
            )

            job_application.save()
            Job.applicants += 1
            Job.save()
            return Response({
                'message': 'Succesfully Applied'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            jobapplication = JobApplication.objects.get(id=pk)
            jobpost = JobPost.objects.get(id=jobapplication.job.id)
            if request.user == jobapplication.user.user:
                jobapplication.delete()
                jobpost.applicants -= 1
                jobpost.save()
                return Response({
                    'message': 'Application canceled'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'no permision to perform this action'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppliedJobsApiView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def get(self, request):
        try:
            userProfile_obj = UserProfile.objects.get(user=request.user)
            applications = JobApplication.objects.filter(
                user=userProfile_obj).order_by('-created')

            serializer = JobApplicationSerializers(applications, many=True)

            return Response({
                'payload': serializer.data,
                'message': 'succes'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
