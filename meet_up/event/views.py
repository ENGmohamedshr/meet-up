

from django.db.migrations import serializer
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from rest_framework.response import Response

from users.serializers import ProfileSerializer

from .serializers import EventSerializer, MemberSerializer
from .models import Event, Member , Place, Category

# Create your views here.


class EventViewSetApi(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    serializer_class = EventSerializer
    
    def list(self,request,*args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk =None, *args, **kwargs):
        try:
            if pk :
                event= Event.objects.get(pk = pk )
                serializer = EventSerializer(event)
                return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            pass
    
    
    @action(detail=False , methods=['post'] , url_path='add-event')
    def addEvent(self,request , *args, **kwargs):
        serializer = EventSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(created_by =request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=True, methods=['get'] , url_path='get-member-profile/(?P<member_id>[^/.])+')
    def get_member(self,request,pk = None ,member_id=None, *args, **kwargs):
        try:
            # event = Event.objects.get(pk=pk)
            member = Member.objects.get(pk =member_id)
            profile = member.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=True , methods=['post'],url_path='join')
    def add_member(self,request,pk = None,*args, **kwargs):
        try:
            
            user = request.user
            event = Event.objects.get(pk=pk)
            # event = self.get_object()
            if not user:
                return Response({'Login':'you must login to get user'},status=status.HTTP_400_BAD_REQUEST)
            if user and event:
                try:
                    member = Member.objects.get(user=user , event =event)
                    if member:
                        return Response('you already in the event' , status=status.HTTP_200_OK)
                except:
                    if event.member_count() < event.num_of_members:
                        Member.objects.create(user = user,event = event)
                        return Response("you are joind ",status=status.HTTP_201_CREATED)
                    else:
                        return Response({'Logic':'Number of users is full in this event'},status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Optionally log the exception here for further debugging
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True , methods=['delete'],url_path='leave')
    def leave_event(self , request , pk = None ,*args, **kwargs):
        event = Event.objects.get(pk = pk )
        user =  request.user
        
        member = Member.objects.get(user=user , event=event)
        serializer =MemberSerializer(member)
        member.delete()
        
        return Response(serializer.data ,status=status.HTTP_204_NO_CONTENT)
    
    
    