

from functools import partial
from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, SignUpSerializer, UserSerializers

# Create your views here.

class UserViewSetApi(viewsets.ViewSet):
    
    @action(detail=False , methods=['post'] , url_path='sign-up')
    def signUp(self,request,*args, **kwargs):
        
        try:
            serializer = SignUpSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            # Optionally log the exception here for further debugging
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']

                if user.is_banned:
                    return Response({'detail': 'You are banned from the application.'}, status=status.HTTP_403_FORBIDDEN)

                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class ProfileViewSetApi(viewsets.ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'],url_path='get-profile')
    def getProfile(self , request , *args, **kwargs):
        try:
            user = request.user
            # profile =get_object_or_404(Profile,user=user)
            if user:
                profile = Profile.objects.get(user=user)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Optionally log the exception here for further debugging
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False , methods=['patch','put'] ,url_path='edit-profile' )
    def editPic(self,request,*args, **kwargs):
        try:
            user = request.user 
            # image = request.data['profile_pic']
            
            profile = Profile.objects.get(user=user)
                
            if profile:
                serializer = ProfileSerializer(profile , request.data , partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data , status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors)
            else:
                return Response({"Profile error":"Profile does't exist"})
        
        except Exception as e:
            # Optionally log the exception here for further debugging
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    