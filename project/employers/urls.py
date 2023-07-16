from django.urls import path
from .import views


urlpatterns = [

    path('view/', views.EmployersHomeView.as_view(), name='view'),
    path('profile-edit/', views.EmployerEditView.as_view(), name='profile-edit'),
    path('add-post/', views.AddPostView.as_view(), name='add-post'),
    path('update-post/<int:pk>/', views.AddPostView.as_view(), name="update-post"),
    path('recruiters-posts/', views.AddPostView.as_view(), name='recruiters-posts'),
    path('delete-post/<int:pk>/', views.AddPostView.as_view(), name="delete-post"),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),


    path('post-plans/', views.BuyPostPlanview.as_view(), name='post-plans'),
    path('buy-plan/',views.BuyPostPlanview.as_view(),name='buy-plan'),

]


