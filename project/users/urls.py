from django.urls import path
from .import views

from rest_framework_simplejwt.views import TokenRefreshView    #type:ignore


urlpatterns = [

#      path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('register/',views.RegisterView.as_view(),name='register'),
     path('verify-email/<str:token>/',views.RegisterView.as_view(),name='verify-email'),
     path('login/',views.LoginView.as_view(),name='login'),
     path('userdetails/',views.UserDetailsView.as_view(),name='userdetails')
]