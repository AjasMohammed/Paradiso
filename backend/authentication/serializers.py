from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'phone']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=validated_data.get('is_staff', False),
            phone=validated_data['phone'],
        )
        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            user_data = {
                'email': email,
                'password': password
            }

            user = authenticate(**user_data)

            if user:
                token = TokenObtainPairSerializer.get_token(user)

                data = {
                    'refresh': str(token),
                    'access': str(token.access_token)
                }

                return data
        raise AuthenticationFailed(
            "Authentication credentials were not provided or are invalid.")
