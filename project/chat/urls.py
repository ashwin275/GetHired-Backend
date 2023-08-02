from django.urls import path
from .import views


urlpatterns = [
    path('messages/<int:pk>/<int:post_id>/',views.ChatMessageApiView.as_view(),name='messages')
]