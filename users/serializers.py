from rest_framework import serializers
from .models import CustomUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'slug', 'email', 'is_verified', 'password', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=60, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'slug', 'email', 'password']

    def create(self, validated_data):
        password = validated_data['password']
        instances = self.Meta.model(**validated_data)
        if password is not None:
            instances.set_password(password)
        instances.save()
        return instances


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=555, min_length=5)
    password = serializers.CharField(max_length=255, min_length=3, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # check for user to authenticate
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid login credentials. Check details and try again.')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled. Contact Admin.')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')
        return {
                'email': user.email,
                'tokens': user.tokens
            }
        return super().validate(attrs)


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=555, min_length=5)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=60, write_only=True)
    token = serializers.CharField(min_length=5, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['password', 'token', 'uidb64']

        def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                id = force_str(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid', 401)
                user.set_password(password=password)
                user.save()
                return user
            except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)
            return super().validate(attrs)