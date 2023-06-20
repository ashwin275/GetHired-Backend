from django.urls import path
from .import views




urlpatterns = [



    # users  manage
    path('admin-view/',views.AdminHomeview.as_view(),name='user-manage'),
     path('user-manage/',views.AdminViewUserManage.as_view(),name='user-manage'),
     path('delete-user/<int:pk>/',views.AdminViewUserManage.as_view(),name='delete-user'),
     path('status-user/<int:pk>/',views.AdminViewUserManage.as_view(),name='status-user'),
     path('employers-manage/',views.AdminViewEmployerManage.as_view(),name='employers-manage'),
    
]