from django.shortcuts import render
from .models import CustomUser, Profile
from .serializers import UserSerializer, VerifyEmailSerializer, UserRegistrationSerializer,SetNewPasswordSerializer, \
    LoginSerializer, RequestPasswordResetEmailSerializer
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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


class UserListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data
            user = CustomUser.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain # left for hardcoded url
            relativeLink = reverse('verify-email')
            absurl = 'http://'+'127.0.0.1:8000'+relativeLink+"?token="+str(token)
            email_body = 'Hi ' + user.first_name + ' use the link below to verify your account \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email address'}
            Util.send_email(data)
            return Response({"success": True, "message": "Account verification email has been sent,"
                                                    " kindly check your email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    serializer = VerifyEmailSerializer()
    token_params_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_params_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated', 'user_id': payload['user_id']}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except User.DoesNotExist:
            Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except User.DoesNotExist:
            Http404

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except User.DoesNotExist:
            Http404

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetEmailSerializer(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain  # left for hardcoded url
            relativeLink = reverse('password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + '127.0.0.1:8000' + relativeLink
            email_body = "Hello, \n use the link below to reset your password \n" + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response({"success": "Check your email for a reset password link"}, status=status.HTTP_200_OK)


class PasswordResetTokenCheck(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is not valid, please request new one" }, status=status.HTTP_200_OK)
            return Response({"success": True, "message":  "credentials is valid", "uidb64": uidb64, "token": token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({"error": "Token is not valid, please request new one"}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(APIView):
    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "message": "Password reset successful"}, status=status.HTTP_200_OK)