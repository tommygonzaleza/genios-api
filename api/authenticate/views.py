from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import permissions, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AuthUserSerializer, GroupSerializer, UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Must include "email" or "username" and "password".'}, status=status.HTTP_403_BAD_REQUEST)
        
        email = email.lower()
        user = User.objects.filter(Q(email__iexact=email) | Q(username=email)).first()
        
        if not user:
            return Response({'error': 'Unable to log in with provided credentials.'}, status=status.HTTP_403_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'error': 'Unable to log in with provided credentials.'}, status=status.HTTP_403_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response('Logged out successfully!', status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]