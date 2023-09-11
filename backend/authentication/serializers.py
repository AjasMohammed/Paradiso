from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_staff', 'phone']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            is_staff = validated_data.get('is_staff', False),
            phone = validated_data['phone'],
        )
        return user


class LogInSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        