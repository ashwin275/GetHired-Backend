from django.urls import path
from .import views

from rest_framework_simplejwt.views import TokenRefreshView    #type:ignore


urlpatterns = [

#      path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('register/',views.RegisterView.as_view(),name='register'),
     path('verify-email/<str:token>/',views.RegisterView.as_view(),name='verify-email'),
     path('login/',views.LoginView.as_view(),name='login'),
     path('userdetails/',views.UserDetailsView.as_view(),name='userdetails'),
     path('logout/', views.LogoutView.as_view(), name='logout'),

     #...............job seeker.................

     path('seeker/view/',views.UserHomeView.as_view(),name='seeker-view'),
     
     path('view-jobs/',views.ViewJobPosts.as_view(),name="view-jobs"),
     path('job-detail/<int:pk>/',views.ViewJobDetails.as_view(),name='job-detail'),

     path('get-experience/',views.ExperienceApiView.as_view(),name='get-experience'),
     path('add-experience/',views.ExperienceApiView.as_view(),name='add-experience'),
     path('update-expereience/<int:pk>/',views.ExperienceApiView.as_view(),name='update-experience'),
     path('delete-expereince/<int:pk>/',views.ExperienceApiView.as_view(),name='delete-expereince')


]