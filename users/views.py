from django.shortcuts import render
from .models import User, Profile
from .serializers import UserSerializer, VerifyEmailSerializer
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


class UserList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain # left for hardcoded url
            relativeLink = reverse('verify-email')
            absurl = 'http://'+'127.0.0.1:8000'+relativeLink+"?token="+str(token)
            email_body = 'Hi ' + user.first_name + ' use the link below to verify your account \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email address'}
            Util.send_email(data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    serializer = VerifyEmailSerializer()
    token_params_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_params_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email': 'Successfully activated', 'user_id': payload['user_id']}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
