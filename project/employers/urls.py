from django.urls import path
from .import views




urlpatterns = [

 path('view/',views.EmployersHomeView.as_view(),name='view'),
 path('profile-edit/',views.EmployerEditView.as_view(),name='profile-edit'),
 path('add-post/',views.AddPostView.as_view(),name='add-post'),
 path('update-post/<int:pk>/',views.AddPostView.as_view(),name="update-post")
    
]