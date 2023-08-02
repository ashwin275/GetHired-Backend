from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message
from django.db.models import Q
from .serializers import MessageSerializer
# Create your views here.


class ChatMessageApiView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self,request,pk,post_id):
        print(request.user.id,pk)
        print(post_id)

        print('called')
        try:
         
            messages = Message.objects.filter((Q(sender = request.user.id)&Q(recipient= pk)&Q(postId=post_id)) | (Q(sender = pk)&Q(recipient = request.user.id)&Q(postId=post_id))).order_by('created_at')
            

            serializer = MessageSerializer(messages,many =True)
            return Response({
                'payload':serializer.data
            },status=status.HTTP_200_OK)

        except:
            pass

        