from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from djoser import views
from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from main_app.models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
 

# Create your views here.


class UserCreate(views.TokenCreateView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyCreate(views.TokenCreateView):
    def post(self, request, format ='json'):
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user.profile

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


 
