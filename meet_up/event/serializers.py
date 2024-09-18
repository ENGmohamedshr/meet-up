

from rest_framework import serializers
from .models import Event, Member


class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True,required=False)
    class Meta:
        model =  Event 
        fields = ['id','topic','num_of_members','category','place','time','members']
        
        
    